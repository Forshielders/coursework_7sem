import { useContext, useEffect } from 'react'
import { CallbackContext, PostContext } from '../../context/MyCustomContext'
import { Button, Form, Input, Spin } from 'antd'
import { Typography } from 'antd'
import { v4 as uuidv4 } from 'uuid'

function MyForm() {
  const { submitHandler, imageLoader } = useContext(CallbackContext)
  const dataObj = useContext(PostContext)
  const { data, image } = dataObj
  const singleDataArr = []
  const doubleDataArr = []
  for (let key in data) {
    if (typeof data[key] !== 'object') {
      singleDataArr.push(key)
    } else {
      doubleDataArr.push(key)
    }
  }

  const [form] = Form.useForm()

  const { Text, Title } = Typography

  const layout = {
    labelCol: { span: 7 },
    wrapperCol: { span: 7 },
  }

  const contentStyle = {
    padding: 50,
    background: 'rgba(0, 0, 0, 0.05)',
    borderRadius: 4,
  }

  const content = <div style={contentStyle} />

  useEffect(() => {
    if (Object.keys(data).length > 0) {
      form.setFieldsValue(data)
    }
  }, [data])

  const onFinish = (values) => {
    submitHandler(values)
    imageLoader()
  }

  return (
    <div style={{ top: 0, display: 'flex', justifyContent: 'space-around' }}>
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
          width: 1000,
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
