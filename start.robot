*** Settings ***
Library    Process    
Library    OperatingSystem
Library    String
Library    file.py


*** Keywords ***
Check for file    
    [Arguments]    ${path}
    File Should Exist    ${path}


*** Test Cases *** 

Run selenium and check if start log contains bitcoin
    ${result} =  Run Process    python    main.py  shell=True  stdout=vm_start_log.txt
    log  ${result.stdout}
    Should Contain  ${result.stdout}    Ethereum
    Should Contain  ${result.stdout}    Bitcoin
    Should Contain  ${result.stdout}    Tether


Test File Exists
    ${file_name}=    Today file name
    ${fileExists}=    File Exists    ${file_name}    
    Check for file    ${file_name}
    Run Keyword If  ${fileExists} is True  Log To Console    Exists!

