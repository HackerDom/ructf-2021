package index

import org.request.NewEmployee

object Tokenizer {
  def getTokens(employee: NewEmployee): List[String] =
    split(employee.description.toLowerCase()) ++
      employee.tags.flatMap(tag => split(tag.toLowerCase())).toSet.toList

  def split(text: String): List[String] = text.split(" +").toList
}
