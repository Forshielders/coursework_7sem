import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import MyCustomContext from './context/PostContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <MyCustomContext>
    <App />
  </MyCustomContext>,
)
