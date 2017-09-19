from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.hue import HueLight


def argument_spec():
    """
    Creates an argument spec for the hue module.
    """
    spec = HueLight.argument_spec()
    spec.update(
        dict(
            bri=dict(
                type='int',
                required=False,
            ),
            sat=dict(
                type='int',
                required=False,
            ),
            transitiontime=dict(
                type='int',
                required=False,
            ),
        )
    )

    return spec


def main():
    m = AnsibleModule(
        argument_spec=argument_spec(),
    )

    hue_light = HueLight(m)

    result = dict(
        changed=False,
        msg='',
    )

    response = hue_light.colorloop(
        bri=m.params.get('bri'),
        sat=m.params.get('sat'),
        transitiontime=m.params.get('transitiontime'),
    )
    result['changed'] = True
    result['msg'] = response.read()

    m.exit_json(**result)


if __name__ == '__main__':
    main()
