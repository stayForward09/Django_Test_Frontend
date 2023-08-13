document.getElementById('whereDropdown').addEventListener('change', function() {
  var value = this.value;

  // Verstecke alle optionalen Elemente und entferne das required-Attribut
  ['categoriesFields', 'typesFields', 'articlesFields'].forEach(function(id) {
    var fields = document.getElementById(id);
    fields.style.display = 'none';
    fields.querySelectorAll('input, select').forEach(function(input) {
      input.required = false;
    });
  });

  // Zeige die entsprechenden Elemente basierend auf der Auswahl und setze das required-Attribut
  if (value === 'categories') {
    var fields = document.getElementById('categoriesFields');
    fields.style.display = 'block';
    fields.querySelectorAll('input, select').forEach(function(input) {
      input.required = false;
    });
  } else if (value === 'types') {
    var fields = document.getElementById('typesFields');
    fields.style.display = 'block';
    fields.querySelectorAll('input, select').forEach(function(input) {
      input.required = false;
    });
  } else if (value === 'articles') {
    var fields = document.getElementById('articlesFields');
    fields.style.display = 'block';
    fields.querySelectorAll('input, select').forEach(function(input) {
      input.required = false;
    });
  }
});
