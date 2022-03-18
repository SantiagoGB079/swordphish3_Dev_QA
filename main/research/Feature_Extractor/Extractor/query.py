
import subprocess
import shlex
import io

#file to execute commands and retrieve its response

def command_query(command='',TimeOut=4):
    """
    command_query() method parsed and execute a command into the system and returns the information obtained.
    This method need two arguments, the command the be executed and Timeout that is the limit time to wait a response
    from the system. The TimeOut argument is set to 4 seconds by default. 
    """

    lis = shlex.split(command)

    if lis == []:

        return 'Command Error'

    else:
            
        dig = subprocess.Popen(lis, stdout=subprocess.PIPE , stderr=subprocess.PIPE,universal_newlines= True)
            
        try:
            
            response = dig.communicate(timeout=TimeOut) #tuple (stdout_data, stderr_data).
            
        except TimeoutError:
            
            dig.kill()
            #response = dig.communicate(timeout=10)
            return "NOt found"
        else:
            
            dig.kill()
            return response[0]
            
        #if dig.returncode != 0 and dig.returncode != 1 and response[-1] != '':
            
        #    return 'Command Error'

        #else:

        #    return response[0]

    
            
#print(command_query(command='whois yahoo.com -h whois.markmonitor.com',TimeOut=10))

#test.command_query('dig yahoo.com +short')
#a = command_query(command='whois yahoo.com -h whois.markmonitor.com',TimeOut=4)
#print(a)

#            error = find_whois_error(response[0])  

#            if  error == "Whois not found":
#                return 'Whois not found'
#            else:
#                if SaveReplyIn == '':
#                    file_management.create_file(file_name='reply.txt')
#                else:
#                    file_management.create_file(file_name=SaveReplyIn)


