$(window).on("offline", function () {
  let ant_alert = localStorage.getItem("ant_alert");
  if (ant_alert) {
      showConnectionLostMessage();
      playBeepSound();
  }
});
function playBeepSound() {
  var audio = new Audio('/files/beep-01a.mp3');
  let beepCount = 0;
  const maxBeeps = 4;
  const beepInterval = setInterval(() => {
      if (!navigator.onLine && beepCount < maxBeeps) {
          audio.play();
          beepCount++;
      } else if (beepCount >= maxBeeps) {
          clearInterval(beepInterval);
      }
  }, 5000);
}

function showConnectionLostMessage() {
  frappe.msgprint('Connection lost! Please check your network connection.');
}

frappe.ui.form.on('Stock Entry Detail', {
  serial_no: function (frm,cdt,cdn) {
      const row=locals[cdt][cdn]
      let serial_no_data = row.serial_no.split("\n");
      let serial_no = serial_no_data[serial_no_data.length - 1];
      frm.set_value('custom_data_serial', serial_no);
  },
  });

frappe.ui.form.on('Stock Entry', {
  onload: function (frm){
    frappe.db.get_single_value("Ant tool Settings", "beep_sound").then(r=>{
      localStorage.setItem("ant_alert",r)
    })
  },
})
  