# grf-analysis-tools
GRF Analysis Tools


```bash
cd grf-analysis-tools
mkdir -p ~/.config/systemd/user/
cp ro-grf-analysis-tools.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable ro-grf-analysis-tools.timer
systemctl --user status ro-grf-analysis-tools.timer
systemctl --user status ro-grf-analysis-tools.service
sudo loginctl enable-linger ec2-user
```
