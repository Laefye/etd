package db

type User struct {
	ID   string `db="ID"`
	Name string `db="Name"`
}

func (t *User) Delete() {
	db.Exec("DELETE FROM `User` WHERE `User`.`ID` = ?", t.ID)
}

func (t *User) UpdateName(username string) {
	db.Exec("UPDATE FROM `User` SET `User`.`Name` = ?", username)
}

func GetAllUsers() []*User {
	values := []*User{}
	db.Select(&value, "SELECT * FROM `User`")
	return values
}
