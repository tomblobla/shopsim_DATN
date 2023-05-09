const template = window.template;
const simList = document.getElementById("sim-grid");
const spinnerBox = document.getElementById("spinner-box");
const loadBtn = document.getElementById("load-btn");
let page = 1;
const handleGetData = () => {
    $.ajax({
        type: "post",
        url: "/load-more-sim/",
        data: { page_number: page, csrfmiddlewaretoken: "{{ csrf_token }}", sim_slug: "{{sim.slug}}" },
        success: function (response) {
            if (response.data === null) { return; }
            const data = response.data;
            spinnerBox.classList.remove("d-none");
            setTimeout(() => {
                spinnerBox.classList.add("d-none");
                data.map(sim => {
                    simList.innerHTML += `
                    <div class="col-md-6 char_col mb-3">
                    <div class="char_item d-flex flex-row align-items-center justify-content-start">
                      <div class="char_icon">
                        <img src="${sim.network_image_logo}" alt="" />
                      </div>
                      <div class="char_content">
                        <div class="char_title font-font-weight-bold">
                          <a class="font-weight-bold" href="">${sim.phone_number}</a>
                        </div>
                        <div class="char_subtitle">
                          {{ sim.get_salepricestr }} {% if sim.discount %}
                          <small class="text-danger">(-{{ sim.discount }}%)</small>
                          {% endif %}
                        </div>
                      </div>
                      <div style="position: absolute; right: 25px; top: 23px; height: 50px; margin: auto;" class="button banner_button my-0">
                        <a href="#" class="valign" style="font-size: 18px; padding: 0px 18px">
                          <i class="fas fa-shopping-cart" style="margin-top: 15px"></i>
                        </a>
                      </div>
                    </div>
                  </div>`;
                })
            }, 500);
        },
        error: function (error) {
            console.log(error);
        },
    });
};

loadBtn.addEventListener("click", () => {
    page += 1;
    handleGetData();
});