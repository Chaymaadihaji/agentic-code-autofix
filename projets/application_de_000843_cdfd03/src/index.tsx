typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { Provider } from 'react-redux';
import store from './store';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import io from 'socket.io-client';

const socket = io();

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <App socket={socket} />
        <ToastContainer />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// server.ts
import express, { Request, Response, NextFunction } from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import morgan from 'morgan';
import passport from 'passport';
import jwt from 'jsonwebtoken';
import userRoutes from './routes/user';
import projectRoutes from './routes/project';
import fileRoutes from './routes/file';
import notificationRoutes from './routes/notification';

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));
app.use(passport.initialize());

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.error('Error connecting to MongoDB:', err));

app.use('/users', userRoutes);
app.use('/projects', projectRoutes);
app.use('/files', fileRoutes);
app.use('/notifications', notificationRoutes);

app.get('/auth/token', (req: Request, res: Response) => {
  const token = req.header('x-auth-token');
  if (!token) return res.status(401).send({ message: 'No token provided' });
  try {
    const decoded = jwt.verify(token, process.env.SECRET_KEY);
    res.send({ message: 'Token is valid', decoded });
  } catch (err) {
    res.status(400).send({ message: 'Invalid token' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

// types.ts
declare module 'express' {
  interface Request {
    user?: any;
  }
}

// user.ts
import mongoose, { Document, Schema } from 'mongoose';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

interface IUser {
  name: string;
  email: string;
  password: string;
}

interface IUserDocument extends IUser, Document {}

const userSchema = new Schema<IUserDocument>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
});

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

userSchema.methods.generateAuthToken = function() {
  const token = jwt.sign({ _id: this._id }, process.env.SECRET_KEY);
  return token;
};

const User = mongoose.model<IUserDocument>('User', userSchema);
export default User;

// project.ts
import mongoose, { Document, Schema } from 'mongoose';

interface IProject {
  title: string;
  description: string;
  user: string;
}

interface IProjectDocument extends IProject, Document {}

const projectSchema = new Schema<IProjectDocument>({
  title: { type: String, required: true },
  description: { type: String, required: true },
  user: { type: Schema.Types.ObjectId, ref: 'User' },
});

const Project = mongoose.model<IProjectDocument>('Project', projectSchema);
export default Project;

// file.ts
import mongoose, { Document, Schema } from 'mongoose';

interface IFile {
  name: string;
  type: string;
  projectId: string;
}

interface IFileDocument extends IFile, Document {}

const fileSchema = new Schema<IFileDocument>({
  name: { type: String, required: true },
  type: { type: String, required: true },
  projectId: { type: Schema.Types.ObjectId, ref: 'Project' },
});

const File = mongoose.model<IFileDocument>('File', fileSchema);
export default File;

// notification.ts
import mongoose, { Document, Schema } from 'mongoose';

interface INotification {
  message: string;
  projectId: string;
}

interface INotificationDocument extends INotification, Document {}

const notificationSchema = new Schema<INotificationDocument>({
  message: { type: String, required: true },
  projectId: { type: Schema.Types.ObjectId, ref: 'Project' },
});

const Notification = mongoose.model<INotificationDocument>('Notification', notificationSchema);
export default Notification;

// socket.ts
import io from 'socket.io-client';

const socket = io();

export default socket;

// store.ts
import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

const initialState = {};

const middleware = [thunk];

const store = createStore(rootReducer, initialState, composeWithDevTools(applyMiddleware(...middleware)));

export default store;

// reducers.ts
import { combineReducers } from 'redux';
import userReducer from './userReducer';
import projectReducer from './projectReducer';
import fileReducer from './fileReducer';
import notificationReducer from './notificationReducer';

const rootReducer = combineReducers({
  user: userReducer,
  project: projectReducer,
  file: fileReducer,
  notification: notificationReducer,
});

export default rootReducer;

// userReducer.ts
import { reducer as formReducer } from 'redux-form';

const initialState = {};

const userReducer = (state = initialState, action) => {
  switch (action.type) {
    default:
      return state;
  }
};

export default userReducer;

// projectReducer.ts
import { reducer as formReducer } from 'redux-form';

const initialState = {};

const projectReducer = (state = initialState, action) => {
  switch (action.type) {
    default:
      return state;
  }
};

export default projectReducer;

// fileReducer.ts
import { reducer as formReducer } from 'redux-form';

const initialState = {};

const fileReducer = (state = initialState, action) => {
  switch (action.type) {
    default:
      return state;
  }
};

export default fileReducer;

// notificationReducer.ts
import { reducer as formReducer } from 'redux-form';

const initialState = {};

const notificationReducer = (state = initialState, action) => {
  switch (action.type) {
    default:
      return state;
  }
};

export default notificationReducer;
