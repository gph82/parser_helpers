import numpy as _np
from fuzzywuzzy import fuzz
from docstring_parser import parse as _docstring_parse
from inspect import signature as _signature
from textwrap import wrap

# https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text

def _inform_of_parser(parser,args=None):
    r"""
    Print all the valuesof the variables in a parser
    TODO find out the native way of doing this
    Parameters
    ----------
    parser

    Returns
    -------

    """
    # TODO is this too hacky, wouldn't *args suffice?
    # This is just to run tests
    if args is None:
        a = parser.parse_args()
    else:
        a = parser.parse_args(args)
    for key, __ in a._get_kwargs():
        dval = parser.get_default(key)
        fmt = '%s=%s,'
        if isinstance(dval, str):
            fmt = '%s="%s",'
        print(fmt % (key, dval))

def _parser2dict(a):
    r"""
    Return a dictionary with the parser properties

    Parameters
    ----------
    a : instantiated parsers, i.e. getattr(parsers,name)()

    Returns
    -------
    dict : dict
        A dictionary with keys like
        ['description', 'arg1', 'arg2', 'kwarg1', 'kwarg2'])

    """
    out = {"description": a.description}
    for ag in a._action_groups:
        #print(ag)
        for ga in ag._group_actions:
            #print(ga)
            #varname = [os.strip("-") for os in ga.option_strings if os.startswith("--")]
            try:
                out[ga.dest] = " ".join(ga.help.splitlines()).replace("  "," ")
            except:
                pass
            #print()
    return out

def _fuzzy_match_dict(key,indict):
    cand_keys = list(indict.keys())

    ratios = [fuzz.ratio(key, key2) for key2 in cand_keys]
    #print("RRR",ratios, indict)
    try:
        best_key = cand_keys[_np.argmax(ratios)]
        print(key, best_key, _np.max(ratios))
        return best_key, indict[best_key]
    except:
        return None, None

def _parser2signature(parsername, method1, alt_method=None):

    parser = eval(parsername)()
    parser_dict = _parser2dict(parser)

    sig1 = _signature(method1)
    sig_keys1 = list(sig1.parameters.keys())

    sig1_docstrs = {pp.arg_name:pp for pp in _docstring_parse(method1.__doc__).params}

    sig_alt_keys = None
    if alt_method is not None:
        sig_alt = _signature(alt_method)
        sig_alt_keys = list(sig_alt.parameters.keys())

        sig_alt_docstrs = {pp.arg_name: pp for pp in _docstring_parse(alt_method.__doc__).params}

    for sig_key in sig_keys1:
        # print(key)
        docstr_key, docstr = _fuzzy_match_dict(sig_key,sig1_docstrs)
        p = sig1.parameters[sig_key]
        if isinstance(p.default, str):
            val = "'%s'" % p.default
        else:
            val = "%s" % str(p.default)
        print("Signature:")
        print("%s : %s, default is %s" % (sig_key, type(p.default).__name__, val))
        print("'%s' %s docstring (BEST match )" % (docstr_key, method1.__name__))
        try:
            print("\n".join(wrap(docstr.description,
                                 60,
                                 initial_indent="        ",
                                 subsequent_indent="        ")))
        except AttributeError:
            print("")
        arg_key, arg_val = _fuzzy_match_dict(sig_key,parser_dict)
        print("'%s' CLI documentation: (BEST match )"%arg_key)
        print("\n".join(wrap(arg_val,
                             60,
                             initial_indent="        ",
                             subsequent_indent="        ")))
        if sig_alt_keys is not None:
            alt_key, alt_val = _fuzzy_match_dict(sig_key,sig_alt_docstrs)
            print("'%s' %s docstring (BEST match )" % (alt_key, alt_method.__name__))
            try:
                print("\n".join(wrap(alt_val.description,
                                     60,
                                     initial_indent="        ",
                                     subsequent_indent="        ")))
            except AttributeError:
                print("")

        input("\n")

def _parser_names():
    return [pp for pp in globals() if pp.startswith("parser_for")]

