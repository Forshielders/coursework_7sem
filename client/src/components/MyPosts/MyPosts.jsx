import { useContext } from 'react'
import { Col, ListGroup, Row } from 'reactstrap'
import MyPostItem from '../MyPostItem'
import { PostContext } from '../../context/PostContext'

function MyPosts() {
  const posts = useContext(PostContext)
  return (
    <Row>
      <Col>
        <ListGroup>
          {posts?.map((el) => (
            <MyPostItem key={el.id} id={el.id} post={el} />
          ))}
        </ListGroup>
      </Col>
    </Row>
  )
}

export default MyPosts
