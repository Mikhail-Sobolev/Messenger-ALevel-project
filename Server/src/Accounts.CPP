
#include <Accounts/Accounts.hpp>

CreateAccountDB() {
    char sql[] = "CREATE TABLE ACCOUNTS(ID INT PRIMARY KEY, NAME CHAR(32), PASSWORD CHAR(64), DESCRIPTION CHAR(256), PFP CHAR(256), NUM_CR INT, CRS INT,NUM_SVRS INT,SVRS INT)";
    sqlite3 *db = sqlite3_open("Accounts.db");
    char *msgerr;
    sqlite3_exec(db, sql, NULL,0,&msgerr);

    sqlite3_close(db);

}

Accounts::Accounts() {
    this->db = sqlite3_open("Accounts.db");
}

Accounts::~Accounts() {
    sqlite3_close(this->db);
}

void Accounts::NewAccount(AccountDetails d) {
    char *msgerr;
    std::string sql = "INSERT INTO ACCOUNTS VALUES(" + d.ID + ", '" + d.Username + "', '" + d.Password + "', '" + d.Description + "', '" + d.Description + "', " + stk::tosql(d.Chatrooms) + ", " + stk::stosql(d.Servers) + ")";
    int exit = sqlite_exec(this->db, sql.c_str(), NULL,0,&msgerr);
}

AccountDetails Accounts::GetAccountDetail() {

    AccountDetails details;
    uint64_t num;

    for (int index = details.Chatrooms.SP; index != 0; index --) {
        num = stk::peek(details.Chatrooms);
        stk::pop(details.Chatrooms);
    }

}