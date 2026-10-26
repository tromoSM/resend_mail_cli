from sys import argv
from resend import api_key,api_url,Emails,exceptions as resendex
import resend
from localstorage import getItem,setItem,LocalstorageFileExists,CreateLocalstorageFile,load
from os import environ,_exit

#resend mailcli
debug=False 
resend_mailcli='1.0.0'
if not LocalstorageFileExists('storage.storage'):
    CreateLocalstorageFile('storage.storage','github.com/tromoSM','tromosm7@gmail.com','tromosm.mailcli.ls')
load('storage.storage')

useenv=False
clearapi=False

if len(argv)>1:
    for arg in argv[1:]:
        arg=arg.replace(' ','').replace('_','').replace('-','').strip().lower()
        if debug:
            print(f'arg > {arg}')
        if arg in ('env','useenv'):
            print('>> using env')
            useenv=True
        if arg in ('v','version'):
            print('RESEND MAILCLI')
            print(f'v{resend_mailcli}\n')
            print('Github : https://github.com/tromoSM/resend_mail_cli')
            _exit(0)
        if arg in ('h','help'):
            print("""
=======================================
            MAILCLI - ARGS
=======================================
""")
            print('debug | dev  :  turn debug mode on')
            print('env | useenv  :  use api key from .env (RESEND_API_KEY) instead of storage file')
            print('v | version : show version of mailcli')
            print('api | showapi : show api key thats being used')
            print('clearapi | refreshapi | removeapi : overwrites the old api key with the api key you provides (doesnt work when using env)')
            print('\nCreate an issue on https://github.com/tromoSM/resend_mail_cli/issues if u have an issue')
            _exit(0)
        if arg in ('debug','dev'):
            print('>> turning debug mode on')
            debug=True
        if arg in ('showapi','api'):
            print(getItem('api') or environ["RESEND_API_KEY"])
            _exit(0)
        if arg in ('clearapi','refreshapi','removeapi'):
            clearapi=True
            print('>> refreshing api key')
if useenv:
    resend.api_key=environ["RESEND_API_KEY"]
else:
    if not getItem('api') or clearapi:
        while True:
            api=input('Resend api key (resend.com/api-keys) : ')
            if len(api.replace(' ','').strip())!=0:
                setItem('api',api)
                print('api key will be saved for future uses')
                break
            else:
                print('>> invalid api key')
    resend.api_key=getItem('api')

if not getItem('accounts'):
    account=input('enter an valid email address to send future mails from : ')
    setItem('accounts',[account])

currentmail=None
print('\n')
accountindex=1
print('[0] Add new a email address')
for account in getItem('accounts'):
    print(f'[{accountindex}] {account}')
    accountindex+=1

print('\n')
fromm=input('Choose an email (from) : ')
if fromm.isdigit() and int(fromm)<=len(getItem('accounts')):
    if int(fromm)==0:
        current:list=getItem('accounts')
        createnew=input('New email address : ')
        current.append(createnew)
        currentmail=createnew
        setItem('accounts',current)
        print(f'>> {createnew} was added.')
    else:
        currentmail=getItem('accounts')[int(fromm)-1]
else:
    print(f'>> value must be a digit and be equal or less than {len(getItem("accounts"))}')
    _exit(0)    
print(f'sending email from {currentmail}')

to=input('Recipient : ')
to=to.split(',')

print(f'sending email to {",".join(to)} {"(multiple)" if len(to)>1 else ""}')
subject=input('Subject : ')

body=input('Body : ')

params:Emails.SendParams={
 "from":currentmail,
 "to":to,
 "subject":subject,
 "text":body
}

print('\n')
print(f'From : {currentmail}')
print(f'To : {",".join(to)} {"(multiple)" if len(to)>1 else ""}')
print(f'Subject : {"(empty)" if len(subject.replace(' ',''))==0 else subject}')
print(f'Body : {body}')

confirm=input('Confirm send (y/N) : ')
confirm=confirm.lower()
if confirm.startswith('y'):
    try:
        status=Emails.send(params)
        print('email sent')
        if debug:
            print(status)

    except resendex.InvalidApiKeyError:
        print(f'api key provided was not valid : {api_key}')
        print(f'start script with "-refreshapi" to enter a new api key.')
    
    except resendex.ResendError as er:
        print(er)
else:
    print('email aborted.')
