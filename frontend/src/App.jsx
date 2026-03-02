import { useState, useEffect } from 'react';
import './App.css'
import { Outlet, createBrowserRouter, RouterProvider } from "react-router-dom";
import Header from "./components/Header"
import Footer from "./components/Footer"

import Index from "./pages/Index"
import Signup from './pages/Signup';
import Login from './pages/Login';

const Content = () => {
  return (
    <>
      <Header />
        <div id='Content'>
          <Outlet />
        </div>
      <Footer />
    </>
  )
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Content />,
    children: [
      {
        index: true,
        element: <Index />
      },
      {
        path: "signup",
        element: <Signup />
      },
      {
        path: "login",
        element: <Login />
      }
    ]
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App
