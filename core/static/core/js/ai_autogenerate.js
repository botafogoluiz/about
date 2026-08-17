// Powers the green "Auto-generate" button on the Profile admin form. Unlike
// the Translate button, this one needs no data from the current page --
// the server pulls Experience/Education/Language directly from the
// database -- so the request body is empty, just a POST.
window.aiAutoGenerateInit = function (opts) {
    document.addEventListener("DOMContentLoaded", function () {
        var btn = document.getElementById("ai-autogenerate-btn");
        if (!btn) return;

        btn.addEventListener("click", function () {
            var confirmed = confirm(
                "Gerar um novo resumo profissional (inglês + português) a partir das " +
                "Experiências, Formações e Idiomas cadastrados?\n\n" +
                "Isso vai substituir o conteúdo atual dos campos de resumo nesta tela."
            );
            if (!confirmed) return;

            btn.disabled = true;
            var originalText = btn.textContent;
            btn.textContent = "Gerando...";

            var csrfInput = document.querySelector('input[name=csrfmiddlewaretoken]');
            var csrfToken = csrfInput ? csrfInput.value : "";

            fetch(opts.generateUrl, {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
            })
                .then(function (resp) {
                    return resp.json().then(function (data) {
                        if (!resp.ok) {
                            throw new Error(data.error || ("HTTP " + resp.status));
                        }
                        return data;
                    });
                })
                .then(function (data) {
                    var enEl = document.getElementById("id_summary_en");
                    var ptEl = document.getElementById("id_summary_pt_br");
                    if (enEl && data.summary_en !== undefined) {
                        enEl.value = data.summary_en;
                        enEl.dispatchEvent(new Event("input", { bubbles: true }));
                        enEl.dispatchEvent(new Event("change", { bubbles: true }));
                    }
                    if (ptEl && data.summary_pt_br !== undefined) {
                        ptEl.value = data.summary_pt_br;
                        ptEl.dispatchEvent(new Event("input", { bubbles: true }));
                        ptEl.dispatchEvent(new Event("change", { bubbles: true }));
                    }
                    alert("Resumo gerado! Revise o conteúdo (inglês e português) e clique em Salvar.");
                })
                .catch(function (err) {
                    alert("Erro ao gerar resumo: " + err.message);
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = originalText;
                });
        });
    });
};
