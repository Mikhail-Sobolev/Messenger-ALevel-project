
#ifndef __inc_accounts_accounts_hpp
#define __inc_accounts_accounts_hpp

#include <stdint.h>
#include <string>
#include <vector>
#include <iostream>
#include <sqlite3.h>
#include <GenDifs/Stack.hpp>

void CreateAccountDB();

typedef struct AccountDetails {
    char Username[32];
    char Password[64];
    char Description[256];
    uint64_t ID;
    char PFP[16][16];
    stack Chatrooms;
    stack Servers;
} AccountDetails;

class Accounts {
public:
    Accounts();
    ~Accounts();

    void NewAccount(AccountDetails a);
    void DeleteAccount(uint64_t ID);
    void ChangeAccountDetail(AccountDetails);
    AccountDetails GetAccountDetail();

private:
    sqlite3* db;
};

#endif