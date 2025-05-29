document.getElementById("san").addEventListener("change", function() {
  const san = this.value;
  const maSelect = document.getElementById("ma");
  maSelect.innerHTML = '<option value="">-- Đang tải --</option>';

  fetch(`/lay-ma-co-phieu?san=${san}`)
    .then(res => res.json())
    .then(data => {
      maSelect.innerHTML = '<option value="">-- Chọn mã --</option>';
      data.forEach(ma => {
        const opt = document.createElement("option");
        opt.value = ma;
        opt.textContent = ma;
        maSelect.appendChild(opt);
      });
    });
});

document.getElementById("btn_du_bao").addEventListener("click", function() {
  const san = document.getElementById("san").value;
  const ma = document.getElementById("ma").value;
  const so_ngay = document.getElementById("so_ngay").value;

  if (!san || !ma || !so_ngay) {
    alert("Vui lòng chọn đầy đủ thông tin và số ngày dự đoán.");
    return;
  }

  window.location.href = `/du-bao?san=${san}&ma=${ma}&so_ngay=${so_ngay}`;
});
