#!/bin/bash

echo "# cuentas-flask" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/aumaza/cuentas-flask.git
git push -u origin main