import { useContext, useEffect } from 'react'
import { CallbackContext, PostContext } from '../../context/MyCustomContext'
import { Button, Form, Input, InputNumber, Space, Spin } from 'antd'
import { Typography } from 'antd'
import { v4 as uuidv4 } from 'uuid'

function MyForm() {
  const { submitHandler, imageLoader } = useContext(CallbackContext)
  const dataObj = useContext(PostContext)
  const { data, image } = dataObj

  console.log(Object.keys(data))
  console.log(data)
  console.log(image)

  const singleDataArr = []
  const doubleDataArr = []
  for (let key in data) {
    if (typeof data[key] !== 'object') {
      singleDataArr.push(key)
    } else {
      doubleDataArr.push(key)
    }
    console.log(`${key}: ${data[key]}`)
  }

  console.log(singleDataArr)
  console.log(doubleDataArr)

  const [form] = Form.useForm()

  const { Text, Title } = Typography

  const layout = {
    labelCol: { span: 7 },
    wrapperCol: { span: 16 },
  }

  const contentStyle = {
    padding: 50,
    background: 'rgba(0, 0, 0, 0.05)',
    borderRadius: 4,
  }

  const content = <div style={contentStyle} />

  /* eslint-disable no-template-curly-in-string */
  const validateMessages = {
    required: '${label} is required!',
    types: {
      email: '${label} is not a valid email!',
      number: '${label} is not a valid number!',
    },
    number: {
      range: '${label} must be between ${min} and ${max}',
    },
  }

  useEffect(() => {
    console.log(data)
    if (Object.keys(data).length > 0) {
      form.setFieldsValue(data)
    }
  }, [data])

  const onFinish = (values) => {
    console.log(values)
    const respData = submitHandler(values)
    imageLoader()
    console.log(respData)
  }

  return (
    <div style={{ top: 0, display: 'flex', justifyContent: 'space-between' }}>
      <div
        style={{
          width: 550,
          height: 500,
          display: 'flex',
          alignContent: 'center',
          flexDirection: 'column',
          flexWrap: 'nowrap',
        }}
      >
        <Title level={3}>Данные для расчетов</Title>
        <Form
          {...layout}
          name="nest-messages"
          onFinish={onFinish}
          style={{ width: 800, marginTop: 20 }}
          validateMessages={validateMessages}
          form={form}
        >
          {singleDataArr.map((el) => (
            <Form.Item
              key={uuidv4()}
              name={[`${el}`]}
              label={el}
              // rules={[{ required: true }]}
            >
              <Input />
            </Form.Item>
          ))}
          {doubleDataArr.map((el) => {
            const value = data[el]
            console.log(el)
            console.log(value)
            return (
              <>
                <Text level={5}>{el}</Text>
                {Object.keys(value).map((data) => (
                  <Form.Item
                    key={uuidv4()}
                    name={[`${el}`, `${data}`]}
                    label={data}
                  >
                    <Input />
                  </Form.Item>
                ))}
              </>
            )
          })}
          <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </div>
      <div
        style={{
          display: 'flex',
          alignContent: 'center',
          flexDirection: 'column',
          flexWrap: 'wrap',
        }}
      >
        <Title level={3}>Графическое представление расчетов</Title>
        {image ? (
          <Input type="image" src={image} style={{}} />
        ) : (
          <Spin style={{ top: 100 }} tip="Loading" size="large">
            {content}
          </Spin>
        )}
      </div>
    </div>
  )
}

export default MyForm
