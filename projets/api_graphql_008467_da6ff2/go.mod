module github.com/nomprojet/api

go 1.19

require (
	github.com/TheBostibn/gqlgen v1.21.1
	github.com/lib/pq v1.10.0
	github.com/dgrijalva/jwt-go v3.2.0
	github.com/go-playground/validator/v10 v10.2.0
)

replace (
	github.com/golang/protobuf v1.4.2 => github.com/golang/protobuf/proto v1.4.2,
)

go modulation

mod .
