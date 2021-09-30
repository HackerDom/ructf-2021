package index
import org.request.{BankCard, Employee, FullName, Location, NewEmployee}
import org.scalatest.FunSuite
import redis.clients.jedis.JedisPool


class IndexTest extends FunSuite {
  test("Runtime.index") {
    val jedisPool = new JedisPool()
    val jedis = jedisPool.getResource
    "random employee description description another worker tag1 tag2 tag3".split(" ").foreach { token =>
      jedis.del(token)
    }
    jedis.close()

    val index = new RuntimeIndex(jedisPool)

    index.index(new Employee(
      id = "716edd0b-9c29-4681-9e1e-4694af0978a8",
      employee = new NewEmployee(
        name = FullName("a", "b", None),
        card = BankCard("123", "card", "sjkd"),
        location = Location("sdf", "kdjf"),
        description = "Random employee description",
        tags = List("tag1", "tag2")
      ),
      owner = "owner"
    )
    )
    index.index(new Employee(
      id = "0f04c1ce-9e2d-4492-8183-3649c625c483",
      employee = new NewEmployee(
        name = FullName("a", "b", None),
        card = BankCard("123", "card", "sjkd"),
        location = Location("sdf", "kdjf"),
        description = "description another worker",
        tags = List("tag1", "tag3")
      ),
      owner = "owner")
    )
    assert(index.search("query") == List())
    assert(index.search("another") == List("0f04c1ce-9e2d-4492-8183-3649c625c483"))
    assert(index.search("description") == List("716edd0b-9c29-4681-9e1e-4694af0978a8", "0f04c1ce-9e2d-4492-8183-3649c625c483"))
    assert(index.search("tag1") == List("716edd0b-9c29-4681-9e1e-4694af0978a8", "0f04c1ce-9e2d-4492-8183-3649c625c483"))
    assert(index.search("tag3") == List("0f04c1ce-9e2d-4492-8183-3649c625c483"))
  }
}
