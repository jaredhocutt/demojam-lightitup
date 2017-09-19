import json

from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.hue import HueLight


def argument_spec():
    """
    Creates an argument spec for the hue module.
    """
    spec = HueLight.argument_spec()

    return spec


def main():
    m = AnsibleModule(
        argument_spec=argument_spec(),
    )

    hue_light = HueLight(m)

    result = dict(
        changed=False,
        light=None,
    )

    response = hue_light.light()
    result['changed'] = True
    result['light'] = json.loads(response.read())

    m.exit_json(**result)


if __name__ == '__main__':
    main()
