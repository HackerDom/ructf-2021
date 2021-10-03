# RuCTF2021 | Employeexer
## Description
Employeexer is a EMPLOYEe indEXER. You can add new employees with personal info. Employeexer index every new employee by desctiption and tags with simple [Inverted Index](https://en.wikipedia.org/wiki/Inverted_index) implementation. Every user can search employees with a search query and see stripped employee partial info (wihout private data).

# Vuln
Every index employeexer makes tokens from desctiption and tags and update index map (token -> employee id) in redis. Salt for user sessions also keeps in the same redis storage. Using one redis storage leads to collision: we can get salt from redis as searched employee id. It only require writing id to same key for bypassing [this check](https://github.com/HackerDom/ructf-2021/blob/main/services/employeexer/app/index/RuntimeIndex.scala#L40). 

# Attack
* Search employee ids by tag `new_employee`;
* Fetch employee infos for getting user nicknames;
* Add new employee with user nicknames in description;
* Search employee ids by user nicknames - it return redis value, which interpreted as salt;
* Generate user secret with nickname and salt;
* Use secret in cookies and get flag in personal info (bank card number).

# Defense 
Use two different redis databases.

