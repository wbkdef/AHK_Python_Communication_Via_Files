#IfWinNotActive, diskfsdiofsd

f_init_polyglot(){
    f_start_python_script()
}

f_log_file_communication(str){
    global file_log_file_communication
    FormatTime, t, , MMddHHmmss
    ; msgbox file_log_file_communication: %file_log_file_communication%
    to_append := "`n" . t . ": " . str
    FileAppend, %to_append%, %file_log_file_communication%
}

f_start_python_script(){
    global file_communication_dir := get_path_dir_AHK() . "\file_communication\"
    global file_communication_to_python_base := file_communication_dir . "to_python"
    global file_communication_return_base := file_communication_dir . "return"
    global file_log_file_communication := file_communication_dir . "log.txt"
    global file_python_stdout_and_error := file_communication_dir . "python_stdout_and_error.txt"

    python_script_path := get_path_dir_python_for_AHK() . "\file_communicators\file_communicator.py"

    f_log_file_communication("`n`n`n")
    f_log_file_communication("------------AHK STARTED---------------")

    command := f_h_python_join(" ", "python", python_script_path, file_communication_dir, file_communication_to_python_base, file_log_file_communication, " > ", file_python_stdout_and_error, " 2>&1")
    f_call_python_fcn_and_return_return_filename("shut_down")
    f_log_file_communication("About to run command:`n" . command . "`n`n")
    sleep 500
    run, %command%, , hide
}


f_call_python_fcn_and_return_results_as_array(args*){
    return_filename := f_call_python_fcn_and_return_return_filename(args*)
    ret := f_get_return_values_from_file(return_filename)
    return ret
}

; space & -::
    fcn := "case_conversion.capitalize_all"
    str := "My Str"
    res := f_call_python_fcn_and_return_results_as_array(fcn, str)
    res_length := res.Length()
    res := res[1]
    msgbox res: %res% of length %res_length%
    return
  

f_call_python_fcn_and_return_result(args*){

    res := f_call_python_fcn_and_return_results_as_array(args*)
    f_t_assert_equal(res.Length(), 1, "f_call_python_fcn_and_return_result returned more than 1 result!")
    return res[1]
}

space & -::
    fcn := "todo_dates.get_review_schedule_basic"
    ; msgbox started
    t_0 := A_TickCount
    res := f_call_python_fcn_and_return_result("todo_dates.get_review_schedule_basic", 1, 2)
    t_2 := A_TickCount
    diff1 := t_2 - t_0
    ; diff2 := t_2 - t_1
    msgbox diff1 %diff1%
    msgbox testing f_call_python_fcn_and_return_result: res: %res%
    return

; space & -::
    ;     fcn := "case_conversion.capitalize_all"
    ;     str := "My Str"
    ;     ; msgbox started
    ;     t_0 := A_TickCount
    ;     sleep 200
    ;     t_1 := A_TickCount
    ;     res := f_call_python_fcn_and_return_result(fcn, str)
    ;     t_2 := A_TickCount
    ;     diff1 := t_1 - t_0
    ;     diff2 := t_2 - t_1
    ;     msgbox diff1 %diff1%  diff2 %diff2%
    ;     msgbox testing f_call_python_fcn_and_return_result: res: %res%
    ;     return


f_call_python_fcn_and_return_return_filename(args*){
    ; The arguments are first the python function name, then the arguments to the python function
    global file_communication_to_python_base

    Random, key, 0, 9999999  ; Make questions for this and the next line  
    return_filename := "return" . key
    args.insertAt(1, return_filename)
    ; __Q: t160409 tp2 t160514 t160723 tp3 t161209 t170914 t190325 tp4 t220413 t280520 tp5 t400802 tp6 rm2.0
        ; generate a random key between 0 & 999, and
        ; add this to the front of array "args"

    to_write_to_file := f_h_python_join(",--,", args*)
    f_log_file_communication("in f_call_python_fcn_and_return_return_filename.  About to write: `n`t" . to_write_to_file)
    ; msgbox about to write %to_write_to_file% to %file_communication_to_python_base%
    file_communication_to_python := file_communication_to_python_base key
    FileAppend %to_write_to_file%, %file_communication_to_python%

    return return_filename
}

f_get_return_values_from_file(filename, max_wait_time=1000, last_mod_time="None"){
    f_log_file_communication("starting f_get_return_values_from_file")
    ret_str := f_get_str_from_file_once_exists(filename, max_wait_time)
    results := f_extract_results_from_str_and_validate_key(filename, ret_str)
    f_log_file_communication("finishing f_get_return_values_from_file, `n`t ret_str:" . ret_str . "`n`t results:" . results)
    return results
}

f_get_str_from_file_once_exists(filename, max_wait_time){
    ; Keeps checking if return_file_name has been modified since last_mod_time up until max_wait_time.

    ; If it has been modified, the contents are returned!
    global  file_communication_dir
    file_path := file_communication_dir . filename
    wait_between_checks := 5
    loops := ceil(max_wait_time/wait_between_checks) + 1
    Loop, %loops% {
        fe := FileExist(file_path)
        ; msgbox fe: %fe%`, file_path: %file_path% 
        if FileExist(file_path){
            FileRead, contents, %file_path% ; There's no function alternative to this!
            return contents
        }
        sleep %wait_between_checks%
    }
    msgbox Waited %max_wait_time% and %file_path% didn't change`n loops is %loops%`, wait_between_checks is %wait_between_checks%
    exit
}

f_extract_results_from_str_and_validate_key(key, ret_str){
    data := StrSplit(ret_str, ",--,")
    key_from_file := data.removeAt(1)
    if (key_from_file=key)
        return data    
    msgbox error - key is %key%`, which doesn't match key_from_file: %key_from_file%.  `n ret_str is %ret_str%
    exit
}


; ---------- Testing --------------
    ; #If f_wg_winactive_sublime_text()
    ; space & ]::
    ;     returned := f_get_return_values_from_file("test_f_get_return_values_from_file", 3000)
    ;     returned1 := returned[1]
    ;     returned2 := returned[2]
    ;     msgbox returned1 is %returned1% `n`n returned2 is %returned2% 
    ;     return
    ; space & [::
    ;     FileAppend, `nanother_line, test_f_get_return_values_from_file
    ;     ; msgbox appended
    ;     return
; =========== End Testing ============

; Deliberative Practice
    ; __Q:  Write this fcn again - can test it with the code below it! 
    deliberative_practice_f_get_return_values_from_file(return_file_name, max_wait_time=1000, last_mod_time="None"){
        ; Keeps checking if return_file_name has been modified since last_mod_time up until max_wait_time.

        ; If it has been modified, the contents are parsed into an array, which is returned!
        if (last_mod_time="None")
            FileGetTime, last_mod_time, %return_file_name%          
        num_loops := Floor(max_wait_time/10)
        loop %num_loops%{
            sleep 10
            FileGetTime, t, %return_file_name%
            if (t<=last_mod_time)
                Continue
            FileRead, contents, %return_file_name%
            data := StrSplit(contents, ",--,")
            return data
        }
        msgbox Waited %max_wait_time% and %return_file_name% didn't change`n loops is %loops%`, wait_between_checks is %wait_between_checks%
    }

    ; ---------- Testing --------------
        ; #If f_wg_winactive_sublime_text()
        ; #IfWinNotActive, kd09sdfkjwf80wenf 
        ; space & ]::
        ;     returned := deliberative_practice_f_get_return_values_from_file("test_deliberative_practice_f_get_return_values_from_file", 3000)
        ;     returned1 := returned[1]
        ;     returned2 := returned[2]
        ;     msgbox returned1 is %returned1% `n`n returned2 is %returned2% 
        ;     return
        ; space & [::
        ;     FileAppend, `,--`,another_line, test_deliberative_practice_f_get_return_values_from_file
        ;     ; msgbox appended
        ;     return
    ; =========== End Testing ============



