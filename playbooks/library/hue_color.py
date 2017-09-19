from ansible.module_utils.basic import AnsibleModule

from ansible.module_utils.hue import HueLight


def argument_spec():
    """
    Creates an argument spec for the hue module.
    """
    spec = HueLight.argument_spec()
    spec.update(
        dict(
            x=dict(
                type='float',
                required=False,
            ),
            y=dict(
                type='float',
                required=False,
            ),
            r=dict(
                type='int',
                required=False,
            ),
            g=dict(
                type='int',
                required=False,
            ),
            b=dict(
                type='int',
                required=False,
            ),
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

    x = m.params.get('x')
    y = m.params.get('y')
    r = m.params.get('r')
    g = m.params.get('g')
    b = m.params.get('b')

    if all(v is not None for v in [x, y]):
        response = hue_light.color_xy(
            x=x,
            y=y,
            bri=m.params.get('bri'),
            sat=m.params.get('sat'),
            transitiontime=m.params.get('transitiontime'),
        )
    elif all(v is not None for v in [r, g, b]):
        response = hue_light.color_rgb(
            r=r,
            g=g,
            b=b,
            bri=m.params.get('bri'),
            sat=m.params.get('sat'),
            transitiontime=m.params.get('transitiontime'),
        )
    else:
        result['msg'] = ('missing required arguments: (x and y) or '
                         '(r and g and b)')
        m.fail_json(**result)

    result['changed'] = True
    result['msg'] = response.read()

    m.exit_json(**result)


if __name__ == '__main__':
    main()
