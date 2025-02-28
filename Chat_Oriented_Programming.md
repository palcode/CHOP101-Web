# Chat-Oriented Programming (CHOP)

## Goal
This document introduces the concept of Chat-Oriented Programming (CHOP), where developers leverage AI-assisted tools to enhance productivity. We will use Cursor AI IDE for demonstrations, but these concepts apply equally to VS Code (with Gemini Code Assist, GitHub Copilot, or relevant extensions) and Vim (using [vimlm](https://github.com/JosefAlbers/vimlm) or [vim-ai](https://github.com/madox2/vim-ai)).

### **OLD DAYS**
![Alt text](./img/RubberDuckProgramming.jpeg)

### **TO NEW WAYS** 

![Alt text](./img/CHOP.jpeg)


## Use Cases & Demonstrations

### **Use Case 1: Generate Boilerplate Code**

**Prompt in Cursor:**  
>“Generate a FastAPI boilerplate with endpoints for CRUD operations on a User model, using SQLite as the database. Add Pydantic validation @Codebase “

### **Use Case 2: Refactor Code** 

**Prompt in Cursor:**  
>“Refactor the code @Codebase to  add user address as well , also do the necessary changes in the rest of the files.”

### **Use Case 3 : Unit test** 

**Prompt in Cursor:**
>“Write pytest unit tests for @Codebase”

### **Use Case 4: Code Understanding and Documentation**

**Prompt in Cursor:**
>“Generate docstring documentation with explanation of the code @Codebase”

### **Use Case 5: Code Review** 

**Prompt in Cursor:**
>“Please do an in-depth code review such that defensive programing is followed , OWASP and other security guidelines are followed , For style guide followed python PEP8  @Codebase “

>“Can you help apply them ?”

### **Use Case 7 : Try to add long extended feature request**

**Prompt in Cursor:**
>Use this code and convert into backend microservice using docker and create a testing frontend in react where user can login via google oauth, and users can manage thier details after login, In future this this is going to be part of a ecommerce application @codebase

>Update the readme with proper instruction on build and test complete application @Codebase


---

## Preferred Tools
- **VS Code** with:
  - [Gemini Code Assist](https://code.google.com/)
  - [GitHub Copilot](https://github.com/features/copilot)
- **Cursor IDE**
- **Vim** with:
  - [vimlm](https://github.com/JosefAlbers/vimlm)
  - [vim-ai](https://github.com/madox2/vim-ai)

---

This document serves as a hands-on guide for developers exploring AI-assisted coding workflows. Feel free to extend these examples as needed!
