package controllers

import com.google.protobuf.InvalidProtocolBufferException
import common.{SessionManager, Store, UserManager, UserManagerException}
import index.RuntimeIndex
import org.request.{Employee, Employees, NewEmployee, UserPair}
import play.api.libs.json.Json
import play.api.mvc.{Cookie, _}
import redis.clients.jedis.JedisPool

import java.io.{ByteArrayInputStream, FileInputStream, InputStream}
import java.nio.file.Paths
import java.util.UUID
import javax.inject._

object Context {
  implicit def parse[T](f: InputStream => T, is: InputStream): Option[T] = try {
    Some(f(is))
  } catch {
    case e: InvalidProtocolBufferException =>
      e.printStackTrace()
      None
  }

  private val jedisPool = new JedisPool()
  val store = new Store(Paths.get("store"))
  val sessionManager = new SessionManager(jedisPool)
  val userManager = new UserManager(jedisPool)
  val index = new RuntimeIndex(jedisPool)
}


@Singleton
class HomeController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  def registerPage(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    Ok(views.html.register())
  }

  def addEmployee(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    withAuth(request, { username =>
      request.body.asRaw match {
        case Some(rawObject) =>
          Context.parse(NewEmployee.parseFrom, new FileInputStream(rawObject.asFile)) match {
            case Some(value) =>
              val employee = new Employee(UUID.randomUUID().toString, value, username)
              Context.store += employee.id -> employee.toByteArray
              Context.index.index(employee)

              Ok(employee.id)
            case None => BadRequest("Incorrect protobuf")
          }
        case None => BadRequest("Incorrect format")
      }
    })
  }

  private def withRequiredParam(param: String, request: Request[AnyContent], block: String => Result): Result = {
    request.getQueryString(param) match {
      case Some(param) => block(param)
      case None => BadRequest(s"Missing required parameter '$param'")
    }
  }

  def fetchEmployeeAsOwner(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    withAuth(request, { username =>
      withRequiredParam("employee_ids", request, { rawEmployee_ids =>
        val employeeIds = rawEmployee_ids.split(',')

        val employees = employeeIds.flatMap { employee_id =>
          Context.store.get(employee_id) match {
            case Some(rawEmployee) =>
              Context.parse(Employee.parseFrom, new ByteArrayInputStream(rawEmployee)) match {
                case Some(employee) => if (employee.owner == username) Some(employee) else None
                case None => None
              }
            case None => None
          }
        }

        if (employees.length == employeeIds.length)
          Ok(new Employees(employees).toByteArray)
        else {
          val existingIds = employees.map { employee => employee.id}.toSet
          val nonExistingIds = employeeIds.filter { employee => !existingIds.contains(employee)}
          BadRequest(s"Incorrect employee ids: ${nonExistingIds.mkString(", ")}")
        }
      })
    })
  }

  def addEmployeePage(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    withAuth(request, { username =>
      Ok(views.html.new_employee("Add new employee", username))
    })
  }

  def loginPage(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    Ok(views.html.login())
  }

  def register(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    request.body.asRaw match {
      case Some(rawObject) =>
        Context.parse(UserPair.parseFrom, new FileInputStream(rawObject.asFile)) match {
          case Some(userPair) =>
            try {
              Context.userManager.addUser(userPair.username, userPair.password)
              setUserCookie(userPair)
            } catch {
              case _: UserManagerException => BadRequest("Incorrect user pair")
            }
          case None => BadRequest("Incorrect protobuf")
        }
      case None => BadRequest("Incorrect format")
    }
  }

  private def setUserCookie(userPair: UserPair): Result = {
    val secret = Context.sessionManager.create(userPair.username)
    Ok("Success").withCookies(Cookie("username", userPair.username), Cookie("secret", secret))
  }

  def login(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    request.body.asRaw match {
      case Some(rawObject) =>
        Context.parse(UserPair.parseFrom, new FileInputStream(rawObject.asFile)) match {
          case Some(userPair) =>
            if (Context.userManager.validateUserPassword(userPair.username, userPair.password)) {
              setUserCookie(userPair)
            } else {
              BadRequest("Incorrect login or password")
            }
          case None => BadRequest("Incorrect protobuf")
        }
      case None => BadRequest("Incorrect format")
    }
  }

  private def withAuth(request: Request[AnyContent], block: String => Result): Result = {
    val secretCookie = request.cookies.get("secret")
    if (secretCookie.isEmpty) {
      return BadRequest("Secret is empty")
    }
    val usernameCookie = request.cookies.get("username")
    if (usernameCookie.isEmpty) {
      return BadRequest("Username cookie is empty")
    }
    val username = usernameCookie.get.value
    if (!Context.sessionManager.validate(username, secretCookie.get.value)) {
      return BadRequest("Invalid cookies")
    }
    block(username)
  }

  def index(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    withAuth(request, { username =>
      Ok(views.html.index("Main", username))
    })
  }

  def searchEmployees(): Action[AnyContent] = Action { implicit request: Request[AnyContent] =>
    withAuth(request, { _ =>
      request.getQueryString("q") match {
        case Some(q) =>
          val ids = Context.index.search(q)
          Ok(Json.toJson(if (ids.isEmpty) "[]" else "[\"" + ids.mkString("\", \"") + "\"]"))
        case None => BadRequest("Missing required parameter 'q'")
      }
    })
  }
}
