if ({{ success }}) { // Hier sollte success aus deinem Django-Context kommen
    var toastEl = document.getElementById('successToast');
    var toast = new bootstrap.Toast(toastEl);
    toast.show();
  }