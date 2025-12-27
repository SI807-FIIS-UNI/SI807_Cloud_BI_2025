#!/bin/bash
# ====================================
# SETUP LIFECYCLE RULES
# ====================================
# Configura reglas de ciclo de vida (Lifecycle) para eliminar
# archivos antiguos (> 30 días) en la carpeta raw/

cat > lifecycle.json <<EOF
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 30, "matchesPrefix": "raw/"}
    }
  ]
}
EOF

gsutil lifecycle set lifecycle.json gs://nettalco-data-bd_grupo05
