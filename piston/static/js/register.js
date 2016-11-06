function checkNotifications() {
  if('PushManager' in window && 'showNotification' in ServiceWorkerRegistration.prototype) {
    document.querySelector(".yes-notifications").classList.remove("hidden");
    document.querySelector(".no-notifications").classList.add("hidden");

    navigator.serviceWorker.register('/serviceworker.js');

    if(Notification.permission == "denied") {
      document.querySelector(".btn-allow").disabled = true;
      document.querySelector(".btn-allow").value = "Not Allowed";
    } else {
      document.querySelector(".btn-allow").disabled = false;
      document.querySelector(".btn-allow").value = "Allow";
    }
  } else {
    document.querySelector(".no-notifications").classList.remove("hidden");
    document.querySelector(".yes-notifications").classList.add("hidden");
  }
}

function onSubmit(e) {
  e.preventDefault();
  Notification.requestPermission().then((response) => {
    if(response == "granted") {
      navigator.serviceWorker.ready.then((serviceWorkerRegistration) => {
        serviceWorkerRegistration.pushManager.subscribe({userVisibleOnly: true}).then((subscription) => {
          document.querySelector("input[name='subscription']").value = JSON.stringify(subscription.toJSON());
          document.querySelector(".approval-form").submit();
        });
      });
    }
  });
}

function init() {
  checkNotifications();
  document.querySelector(".approval-form").addEventListener('submit', onSubmit);
}


init();
