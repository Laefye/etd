{'t': 'ARG', 'type': 'string', 'name': 'id', 's': 1}
package db

type User struct {
	ID string `db="ID"`
	Username string `db="Username"`
	Email string `db="Email"`
	CreatedAt int `db="CreatedAt"`
}

func NewUser(id string) User {
	value := &User{}
