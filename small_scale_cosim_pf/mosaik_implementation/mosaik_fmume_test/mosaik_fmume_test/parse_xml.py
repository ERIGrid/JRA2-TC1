'''Helper script that reads variable information from
the modelDescription.xml file of an FMU.'''
import xml.etree.ElementTree as ETree
import fmipp

def get_var_table(filename):
    var_table = {}
    translation_table = {}

    base = ETree.parse(filename).getroot()
    mvars = base.find('ModelVariables')

    for var in mvars.findall('ScalarVariable'):
        causality = var.get('causality')
        name = var.get('name')
        if causality in ['input', 'output', 'parameter']:
            var_table.setdefault(causality, {})
            translation_table.setdefault(causality, {})
            # Variable names with '.' do not work in Python,
            # the symbol has to be replaced by '_':
            if '.' in name:
                alt_name = name.replace('.', '_')
            else:
                alt_name = name
            # The translation table maps between FMU name and Python name
            translation_table[causality][alt_name] = name

            # Some modelers use input and parameter variables for the same purpose
            # So inputs have to be listed as possible parameter and vice versa
            if causality == 'input':
                var_table.setdefault('parameter', {})
                translation_table.setdefault('parameter', {})
                translation_table['parameter'][alt_name] = name
            if causality == 'parameter':
                var_table.setdefault('input', {})
                translation_table.setdefault('input', {})
                translation_table['input'][alt_name] = name

            specs = var.getchildren()
            for spec in specs:
                if spec.tag in ['Real', 'Integer', 'Boolean', 'String']:
                    var_table[causality][name] = spec.tag
                    if causality == 'input':
                        var_table['parameter'][name] = spec.tag
                    if causality == 'parameter':
                        var_table['input'][name] = spec.tag
                    continue

    return var_table, translation_table
