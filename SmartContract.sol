// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

contract SmartContract {

    // ================= FILE OWNER REGISTRATION =================
    // Used by AuthorizerApp to track File Owners
    struct Register {
        uint id;
        string data;  
        /*
        format:
        ownerAddress#ownerName#email#status#timestamp
        */
    }

    Register[] private register;


    // ================= FILE UPLOAD VERIFICATION =================
    // Used by FileOwnerModule
    struct FileUpload {
        uint id;
        string data;
        /*
        format:
        ownerAddress#fileHash#ipfsHash#token#timestamp
        */
    }

    FileUpload[] private fileupload;


    // ================= RECOVERY & TRUST MONITORING =================
    // Used by RecoveryModule
    struct RecoveryLog {
        uint id;
        string data;
        /*
        format:
        ownerAddress#fileHash#action#status#timestamp
        action = deleted | requested | recovered | verified
        */
    }

    RecoveryLog[] private recoverylog;


    // =======================================================
    // ================= FILE OWNER REGISTRATION =============
    // =======================================================

    function setRegister(string memory _data) public {
        uint _id = register.length;
        register.push(Register(_id, _data));
    }

    function getRegister() public view returns (Register[] memory) {
        return register;
    }


    // =======================================================
    // ================= FILE UPLOAD =========================
    // =======================================================

    function setFile(string memory _data) public {
        uint _id = fileupload.length;
        fileupload.push(FileUpload(_id, _data));
    }

    function getFile() public view returns (FileUpload[] memory) {
        return fileupload;
    }


    // =======================================================
    // ================= RECOVERY LOGGING ====================
    // =======================================================

    function addRecoveryLog(string memory _data) public {
        uint _id = recoverylog.length;
        recoverylog.push(RecoveryLog(_id, _data));
    }

    function getRecoveryLog() public view returns (RecoveryLog[] memory) {
        return recoverylog;
    }

}
