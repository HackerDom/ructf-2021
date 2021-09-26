package common

import redis.clients.jedis.JedisPool

import scala.util.Random


class SessionManager(private val jedisPool: JedisPool) extends WithJedis(jedisPool) {
  def create(username: String): String = {
    val salt = "salt/" + Random.alphanumeric.take(32).mkString("")
    val secret = Utils.baseHash(username + salt)

    withJedis { jedis =>
      jedis.set(username, salt)
    }
    secret
  }

  def delete(username: String): Unit = {
    try {
      withJedis { jedis =>
        jedis.del(username)
      }
    } catch {
      case _: Throwable =>
    }
  }

  def validate(username: String, secret: String): Boolean = {
    withJedis { jedis =>
      val salt = jedis.get(username)
      if (salt == null) false
      else Utils.baseHash(username + salt) == secret
    }
  }
}
