go
type Mutation {
  register(username: String!, email: String!): User
  login(email: String!, password: String!): Auth
}

type Query {
  getUser(id: ID!): User
}

type Subscription {
  message: Message!
}

input User {
  id: ID!
  username: String
  email: String
}
