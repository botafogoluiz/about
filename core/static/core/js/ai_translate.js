// Powers the red "Translate" button on admin add/change forms for any model
// using TranslateAdminMixin. Finds every *_pt_br <-> *_en field pair on the
// page by naming convention, sends the pt-br values to the model's
// translate-fields/ endpoint (Claude), and writes the results back into the
// _en fields -- including CKEditor5-managed rich text fields, via the
// window.editors[id] registry django-ckeditor-5 exposes.
window.aiTranslateInit = function (opts) {
    document.addEventListener("DOMContentLoaded", function () {
        var btn = document.getElementById("ai-translate-btn");
        if (!btn) return;

        function isCkeditorField(fieldName) {
            return opts.ckeditorFields.indexOf(fieldName) !== -1;
        }

        function readValue(id, isHtml) {
            if (isHtml && window.editors && window.editors[id]) {
                return window.editors[id].getData();
            }
            var el = document.getElementById(id);
            return el ? el.value : "";
        }

        function writeValue(id, isHtml, text) {
            if (isHtml && window.editors && window.editors[id]) {
                window.editors[id].setData(text);
                return;
            }
            var el = document.getElementById(id);
            if (!el) return;
            el.value = text;
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }

        btn.addEventListener("click", function () {
            var ptInputs = document.querySelectorAll('[id^="id_"][id$="_pt_br"]');
            var pairs = [];

            ptInputs.forEach(function (ptEl) {
                var ptId = ptEl.id;
                var ptFieldName = ptId.slice(3); // strip "id_"
                var baseId = ptId.slice(0, -6); // strip "_pt_br"
                var enId = baseId + "_en";
                var enFieldName = enId.slice(3);
                var enEl = document.getElementById(enId);
                if (!enEl) return;

                var isHtml = isCkeditorField(ptFieldName);
                var ptText = readValue(ptId, isHtml);
                if (!ptText || !ptText.trim()) return;

                pairs.push({
                    ptId: ptId,
                    enId: enId,
                    isHtml: isCkeditorField(enFieldName) || isHtml,
                    text: ptText,
                });
            });

            if (pairs.length === 0) {
                alert("Nenhum campo em português com conteúdo pra traduzir.");
                return;
            }

            var fieldLabel = pairs.map(function (p) { return p.ptId.replace(/^id_/, ""); }).join(", ");
            var confirmed = confirm(
                "Traduzir " + pairs.length + " campo(s) de português para inglês (" + fieldLabel + ")?\n\n" +
                "Isso vai substituir qualquer conteúdo em inglês já existente nesses campos."
            );
            if (!confirmed) return;

            btn.disabled = true;
            var originalText = btn.textContent;
            btn.textContent = "Traduzindo...";

            var fieldsPayload = {};
            var htmlFieldsPayload = [];
            pairs.forEach(function (p) {
                fieldsPayload[p.ptId] = p.text;
                if (p.isHtml) htmlFieldsPayload.push(p.ptId);
            });

            var csrfInput = document.querySelector('input[name=csrfmiddlewaretoken]');
            var csrfToken = csrfInput ? csrfInput.value : "";

            fetch(opts.translateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ fields: fieldsPayload, html_fields: htmlFieldsPayload }),
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
                    pairs.forEach(function (p) {
                        var translated = data[p.ptId];
                        if (translated === undefined) return;
                        writeValue(p.enId, p.isHtml, translated);
                    });
                    alert("Tradução concluída! Revise o conteúdo em inglês e clique em Salvar.");
                })
                .catch(function (err) {
                    alert("Erro ao traduzir: " + err.message);
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = originalText;
                });
        });
    });
};
