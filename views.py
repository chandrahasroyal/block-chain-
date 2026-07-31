import os
import hashlib
import time
import ipfsapi
from django.shortcuts import render, redirect
from BlockchainFiles import Records


# Create your views here.
def login(request):
    return render(request,'R/Login.html')

def Log_Action(request):
    if request.method=='POST':
        uname = request.POST['username']
        pwd =  request.POST['password']

        if uname == 'Recovery' and pwd =='Recovery':
            return render(request,'R/Home.html')
        else:
            context={"msg":"Login failed please try again..!!"}
            return render(request,'R/Login.html',context)

def home(request):
    return render(request, 'R/Home.html')



def recovery_requests(request):
    records = Records.getRecords('recovery')

    requests = []

    for r in records:
        data = r[1].split("#")

        # format:
        # email#fileHash#ipfsHash#REQUESTED#timestamp
        if data[3] == "REQUESTED":
            requests.append({
                'email': data[0],
                'hash': data[1],
                'ipfs': data[2],
                'time': data[4]
            })

    return render(request, 'R/All_Request.html',
                  {'requests': requests})

# IPFS connection (same as your upload logic)
api = ipfsapi.Client(host='http://127.0.0.1', port=5001)

def recover_file(request):
    if request.method == 'POST':

        email = request.POST['email']
        file_hash = request.POST['file_hash']
        ipfs_hash = request.POST['ipfs_hash']

        # 🔍 Step 0: Check existing recovery logs
        recovery_logs = Records.getRecords('recovery') or []

        for r in recovery_logs:
            data = r[1].split("#")
            if data[0] == email and data[1] == file_hash:
                if data[3] == "RECOVERED":
                    return render(request, 'R/All_Request.html', {
                        'msg': 'This file has already been recovered.'
                    })

        try:
            # 1. Fetch file from IPFS
            recovered_data = api.get_pyobj(ipfs_hash)

            # 2. Verify hash integrity
            verify_hash = hashlib.sha256(recovered_data).hexdigest()
            if verify_hash != file_hash:

                # 🔴 LOG FAILED RECOVERY ATTEMPT
                timestamp = str(int(time.time()))
                log_data = (
                    email + "#" +
                    file_hash + "#" +
                    ipfs_hash + "#" +
                    "FAILED" + "#" +
                    timestamp
                )
                Records.saveRecords(log_data, 'recovery')

                return render(request, 'R/All_Request.html', {
                    'msg': 'Hash mismatch! Recovery failed and logged.'
                })

            # 3. Save recovered file (only once)
            recovery_path = "recovery_storage"
            if not os.path.exists(recovery_path):
                os.makedirs(recovery_path)

            filename = file_hash[:10] + "_recovered"
            file_path = os.path.join(recovery_path, filename)

            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(recovered_data)

            # 4. Log RECOVERED event
            timestamp = str(int(time.time()))
            log_data = (
                email + "#" +
                file_hash + "#" +
                ipfs_hash + "#" +
                "RECOVERED" + "#" +
                timestamp
            )
            Records.saveRecords(log_data, 'recovery')

            return render(request, 'R/All_Request.html', {
                'msg': 'File Successfully Recovered and Stored on local space.'
            })

        except Exception:
            return render(request, 'R/All_Request.html', {
                'msg': 'Recovery failed due to IPFS error.'
            })


def recovered_files(request):

    records = Records.getRecords('recovery')

    recovered = []

    for r in records:
        data = r[1].split("#")

        # format:
        # email#fileHash#ipfsHash#RECOVERED#timestamp
        if data[3] == "RECOVERED":
            recovered.append({
                'email': data[0],
                'hash': data[1],
                'ipfs': data[2],
                'time': data[4],
                'status': data[3]
            })

    return render(request, 'R/Recovered.html',
                  {'files': recovered})
