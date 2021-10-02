package common


class UserManagerException(message: String) extends Exception(message)


class UserManager(private val store: Store) {
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
    if (store.get(s"user/$username").isDefined) {
      throw new UserManagerException("User is already exist")
    }
  }

  def addUser(username: String, password: String): Unit = {
    validateUserPair(username, password)
    validateExisting(username)

    val passwordHash = Utils.baseHash(password)
    store += s"user/$username" -> passwordHash.getBytes()

  }

  def validateUserPassword(username: String, password: String): Boolean = {
    store.get(s"user/$username") match {
      case Some(passwordHash) => Utils.baseHash(password) == new String(passwordHash)
      case None => false
    }
  }
}
