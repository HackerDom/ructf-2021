package common

import redis.clients.jedis.JedisPool

class UserManagerException(message: String) extends Exception(message)


class UserManager(jedisPool: JedisPool) extends WithJedis(jedisPool) {
  private val usernameRegex = "[0-9a-zA-Z]{1,20}".r

  def validateUserPair(username: String, password: String): Unit = {
    if (!usernameRegex.matches(username)) {
      throw new UserManagerException("Incorrect username")
    }

    if (!usernameRegex.matches(password)) {
      throw new UserManagerException("Incorrect password")
    }
  }

  def validateExisting(username: String): Unit = {
    withJedis { jedis =>
      if (jedis.get(s"user/$username") != null) {
        throw new UserManagerException("User is already exist")
      }
    }
  }

  def addUser(username: String, password: String): Unit = {
    validateUserPair(username, password)
    validateExisting(username)

    withJedis { jedis =>
      val passwordHash = Utils.baseHash(password)
      jedis.set(s"user/$username", passwordHash)
    }
  }

  def validateUserPassword(username: String, password: String): Boolean = {
    println(username)
    println(password)
    withJedis { jedis =>
      val passwordHash = jedis.get(s"user/$username")
      println(passwordHash)
      if (passwordHash == null) {
        false
      } else {
        println(Utils.baseHash(password))
        Utils.baseHash(password) == passwordHash
      }
    }
  }
}
