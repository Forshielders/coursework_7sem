import { useContext, useState } from 'react'

import './App.css'
import { PostContext } from './context/PostContext'
import MyForm from './components/MyForm/MyForm'

function App() {
  const posts = useContext(PostContext)

  console.log(posts)

  return (
    <>
      <MyForm />
    </>
  )
}

export default App
