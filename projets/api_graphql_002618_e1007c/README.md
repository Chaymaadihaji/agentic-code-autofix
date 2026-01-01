graphql
type Query {
  articles: [Article]
  article(id: Int!): Article
  users: [User]
  user(id: Int!): User
  comments: [Comment]
  comment(id: Int!): Comment
}

type Mutation {
  createArticle(title: String!, content: String!): Article
  updateArticle(title: String!, content: String!, id: Int!): Article
  deleteArticle(id: Int!): Boolean
  createUser(name: String!, email: String!): User
  updateUser(name: String!, email: String!, id: Int!): User
  deleteUsers(ids: [Int!]!): [Boolean!]!
  createComment(content: String!, articleId: Int!): Comment
  updateComment(content: String!, id: Int!): Comment
  deleteComment(id: Int!): Boolean
}
