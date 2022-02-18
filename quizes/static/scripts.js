function addField() {
  var field = document.createElement("input");
  field.setAttribute("type", "text");
  // name attribute has to be equal to variable name in forms.py
  field.setAttribute("name", "incorrect_answer");
  field.setAttribute("label", "Incorrect Answer");
  field.setAttribute("class", "form-control with-break");

  document.getElementsByName("form-fields")[0]
  .appendChild(field)

  document.getElementById('form-fields').innerHTML += '<br>'

}

