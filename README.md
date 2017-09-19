# Demo Jam: Light It Up

This is a WIP for a demo of how to use Ansible to control Philips Hue light bulbs.

## How to use

### Install dependencies

```bash
pip install -r requirements.txt
```

### Export environment variables

```bash
export HUE_IP=192.168.1.100
export HUE_USER=58d97fc1faab1adddaccf59a0e1443b0
```

### Make your own playbook

1. Use the example playbook as a reference (`playbooks/main.yaml`)
2. Use the custom modules to turn your lights on/off and change colors
    - `hue_on`
    - `hue_off`
    - `hue_color`
    - `hue_colorloop`
