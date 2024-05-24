import axios from 'axios'
import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import PropTypes from 'prop-types'

const PostContext = createContext()
const CallbackContext = createContext()

function MyCustomContext({ children }) {
  const [data, setData] = useState([])
  const [image, setImage] = useState(null)

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/config').then((resp) => {
      console.log(resp)
      setData(resp.data)
    })
  }, [])

  console.log(data)
  const submitHandler = useCallback(async (e, input) => {
    e.preventDefault()
    const resp = await axios.post('http://127.0.0.1:5000/config', {
      payload: input,
    })
    setData((prev) => [...prev, resp.data])
  }, [])

  const imageLoader = useCallback(async (e, input) => {
    e.preventDefault()
    const resp = await axios.get('http://127.0.0.1:5000/plot', {
      payload: input,
    })
    setImage(resp.data)
  }, [])

  const handlers = useMemo(() => ({ submitHandler, imageLoader }), [])

  return (
    <CallbackContext.Provider value={handlers}>
      <PostContext.Provider value={(data, image)}>
        {children}
      </PostContext.Provider>
    </CallbackContext.Provider>
  )
}

MyCustomContext.propTypes = {
  children: PropTypes.node.isRequired,
}

export { PostContext, CallbackContext }
export default MyCustomContext
