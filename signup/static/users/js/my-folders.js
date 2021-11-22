/* window.onload = () => {
    const tab_switchers = document.querySelectorAll('[data-switcher]');

    for (let i = 0; i < tab_switchers.length; i++) {
        const tab_switcher = tab_switchers[i];
        const page_id = tab_switcher.dataset.tab;

        tab_switcher.addEventListener('click', () => {
            document.querySelector('.tabs .tab.is-active').classList.remove('is-active');
            tab_switcher.parentNode.classList.add('is-active');

            SwitchPage(page_id);
        });
    }
}

function SwitchPage (page_id) {
    console.log(page_id);

    const current_page = document.querySelector('.pages .page.is-active');
    current_page.classList.remove('is-active');

    const next_page = document.querySelector(`.pages .page[data-page="${page_id}"]`);
    next_page.classList.add('is-active');
} */

function clickEditOnAnnotation(id) {
    if(document.getElementById("pubsAnnotationTextArea_"+id).hasAttribute('readonly'))
        document.getElementById("pubsAnnotationTextArea_"+id).removeAttribute('readonly');
    else
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);

    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    if (save.style.display === "none" && cancel.style.display === "none") {
      save.style.display = "inline";
      cancel.style.display = "inline";
    } else {
      save.style.display = "none";
      cancel.style.display = "none";
    }

    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    edit.style.display = "none";
    del.style.display = "none";
}

function clickCancelAnnotation(id){
    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);
}

function setupTabs(){
    document.querySelectorAll('.tabs-button').forEach(button => {
        button.addEventListener('click', () => {
            const sideBar = button.parentElement;
            const tabsCon = sideBar.parentElement;
            const tabNum = button.dataset.forTab;
            const tabToActivate = tabsCon.querySelector(`.tabs-content[data-tab="${tabNum}"]`);

            sideBar.querySelectorAll(".tabs-button").forEach(button => {
                button.classList.remove("tabs-button-active");
            });

            tabsCon.querySelectorAll(".tabs-content").forEach(tab => {
                tab.classList.remove("tabs-content-active");
            });

            button.classList.add("tabs-button-active");
            tabToActivate.classList.add("tabs-content-active");
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupTabs();
});