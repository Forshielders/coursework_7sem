import axios from 'axios'
import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import PropTypes from 'prop-types'
import { saveAs } from 'file-saver'

const PostContext = createContext()
const CallbackContext = createContext()

function MyCustomContext({ children }) {
  const [data, setData] = useState({})
  const [image, setImage] = useState(null)

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/config').then((response) => {
      setData(response.data)
    })
  }, [])

  useEffect(() => {
    if (Object.keys(data).length > 0) {
      // imageLoader()
    }
  }, [data])

  const submitHandler = useCallback(async (data) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/config', {
        data,
      })
      console.log('Ответ от сервера: ', response.data)
      const fileData =
        typeof response.data === 'string'
          ? response.data
          : JSON.stringify(response.data, null, 2)

      const blob = new Blob([fileData], { type: 'text/plain;charset=utf-8' })

      saveAs(blob, 'config.txt')
    } catch (error) {
      console.error('Ошибка при получении config: ', error)
    }
  }, [])

  const imageLoader = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/plot', {
        responseType: 'blob',
      })
      const imageBlob = response.data
      const imageObjectURL = URL.createObjectURL(imageBlob)
      setImage(imageObjectURL)
    } catch (error) {
      console.error('Ошибка при получении изображения: ', error)
    }
  }, [])

  const dataObj = { data: data, image: image }

  const handlers = useMemo(() => ({ submitHandler, imageLoader }), [])

  return (
    <CallbackContext.Provider value={handlers}>
      <PostContext.Provider value={dataObj}>{children}</PostContext.Provider>
    </CallbackContext.Provider>
  )
}

MyCustomContext.propTypes = {
  children: PropTypes.node.isRequired,
}

export { PostContext, CallbackContext }
export default MyCustomContext
