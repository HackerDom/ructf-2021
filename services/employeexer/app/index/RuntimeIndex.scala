package index

import common.WithJedis
import org.request.Employee
import redis.clients.jedis.{JedisPool, Transaction}

import scala.collection.mutable

class RuntimeIndex(private val jedisPool: JedisPool) extends WithJedis(jedisPool) {
  def index(employee: Employee): Unit = {
    val tokens = Tokenizer.getTokens(employee.employee)
    withJedisTransaction(tokens, { jedis =>

      val tokenMap = scala.collection.mutable.Map[String, mutable.Set[String]]()
      tokens.foreach { token =>
        val jedisRecord = jedis.get(token)
        val employeeIds = if (jedisRecord != null) mutable.Set[String](jedisRecord.split(" "):_*) else mutable.Set[String]()
        employeeIds += employee.id
        tokenMap += token -> employeeIds
      }
      tokenMap
    }, { (tokenMap: scala.collection.mutable.Map[String,scala.collection.mutable.Set[String]], transaction) =>
      tokenMap.toList.foreach { tokenWithIds =>
        transaction.set(tokenWithIds._1, tokenWithIds._2.mkString(" "))
      }
    })

    tokens.foreach { token =>
      withJedis { jedis =>
        jedis.set("idx/" + token, "idx")
      }
    }
  }

  def search(text: String): List[String] = {
    val employeeIds = mutable.Set[String]()

    Tokenizer.split(text).foreach { token =>
      withJedis { jedis =>
        if (jedis.get("idx/" + token) == "idx") {
          val relatedIdsRecord = jedis.get(token)
          if (relatedIdsRecord != null) {
            employeeIds.addAll(relatedIdsRecord.split(" "))
          }
        }
      }
    }
    employeeIds.toList
  }
}
