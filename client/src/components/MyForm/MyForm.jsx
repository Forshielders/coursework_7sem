import { useContext, useEffect } from 'react'
import { CallbackContext, PostContext } from '../../context/PostContext'
import { Button, Form, Input, InputNumber, Space, Spin } from 'antd'
import { Typography } from 'antd'

function MyForm() {
  const { submitHandler, imageLoader } = useContext(CallbackContext)
  const data = useContext(PostContext)
  const image = useContext(PostContext)

  console.log(data)

  const [form] = Form.useForm()

  const { Title } = Typography

  const layout = {
    labelCol: { span: 6 },
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

  const user = {
    user: {
      name: 'okd',
      email: 'vasya@yandex.ru',
      age: '32',
      website: 'https://www.google.com',
      introduction: { data: 'o-gogo' },
    },
  }

  useEffect(() => {
    form.setFieldsValue(user)

    // if (data && data?.length > 0) {
    //   form.setFieldsValue(user)
    // }
  }, [])

  const onFinish = (values) => {
    console.log(values)
    const respData = submitHandler(values)
    console.log(respData)
  }

  return (
    <div style={{ top: 0, display: 'flex' }}>
      <div
        style={{
          width: 550,
          display: 'flex',
          alignContent: 'center',
          flexDirection: 'column',
          flexWrap: 'wrap',
        }}
      >
        <Title level={3}>Данные для расчетов</Title>
        <Form
          {...layout}
          name="nest-messages"
          onFinish={onFinish}
          style={{ width: 700, marginTop: 20 }}
          validateMessages={validateMessages}
          form={form}
        >
          <Form.Item
            name={['user', 'name']}
            label="Name"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name={['user', 'email']}
            label="Email"
            rules={[{ type: 'email' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name={['user', 'age']}
            label="Age"
            rules={[{ type: 'number', min: 0, max: 99 }]}
          >
            <InputNumber />
          </Form.Item>
          <Form.Item name={['user', 'website']} label="Website">
            <Input />
          </Form.Item>
          <Form.Item
            name={['user', 'introduction', 'data']}
            label="Introduction"
          >
            <Input.TextArea />
          </Form.Item>
          <Form.Item wrapperCol={{ ...layout.wrapperCol, offset: 8 }}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </div>
      <div
        style={{
          width: '100%',
          display: 'flex',
          alignContent: 'center',
          flexDirection: 'column',
          flexWrap: 'wrap',
        }}
      >
        <Title level={3}>Графическое представление расчетов</Title>
        {image ? (
          <Input type="image" src={image} />
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
