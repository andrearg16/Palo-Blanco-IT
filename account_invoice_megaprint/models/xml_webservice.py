# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement

from odoo import models

import logging

_logger = logging.getLogger( __name__ )


class AccountInvoice(models.Model):
    _inherit = "account.move"

    def GenerateXML_FCAM(self, _moneda, _fechayhora, _numeroacceso, _tipo, _afiIVA, _estabCode, _mailEmi, _NITEmisor, _NombreComercial, _NombreEmisor,
                         _calleEmisor, _postalEmisor, _muniEmisor, _deptoEmisor, _paisEmisor, _mailRec, _IDReceptor, _NombreReceptor, _calleRecept,
                         _postalRecept, _muniRecept, _deptoRecept, _paisRecept, _frases, _items, _iva, _total, _uuId, Complemento_Data, AdendaSummaryData):

        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        fe.set('Version', '0.1')

        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')

        DTE.set('ID', 'DatosCertificados')
        # minimo = SubElement(documento, 'minimo')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', _moneda)
        DatosGenerales.set('FechaHoraEmision', _fechayhora)
        DatosGenerales.set('NumeroAcceso', _numeroacceso)
        DatosGenerales.set('Tipo', _tipo)

        # Emisor
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        Emisor.set('AfiliacionIVA', _afiIVA)
        Emisor.set('CodigoEstablecimiento', _estabCode)
        Emisor.set('CorreoEmisor', _mailEmi)
        Emisor.set('NITEmisor', _NITEmisor)
        Emisor.set('NombreComercial', _NombreComercial)
        Emisor.set('NombreEmisor', _NombreEmisor)

        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = str(_calleEmisor)

        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = str(_postalEmisor)

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = str(_muniEmisor)

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = str(_deptoEmisor)

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = str(_paisEmisor)

        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', _mailRec)
        Receptor.set('IDReceptor', _IDReceptor)
        Receptor.set('NombreReceptor', _NombreReceptor)

        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = str(_calleRecept)

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = str(_postalRecept)

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = str(_muniRecept)

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = str(_deptoRecept)

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = str(_paisRecept)

        # FRASES
        frases = SubElement(DatosEmision, 'dte:Frases')
        for phrase in _frases:
            frase = SubElement(frases, 'dte:Frase')
            frase.set('CodigoEscenario', str(phrase[0]))
            frase.set('TipoFrase', str(phrase[1]))

        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        for prod in _items:
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', str(prod[0]))
            item.set('NumeroLinea', str(prod[1]))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = str(prod[2])
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = str(prod[3])
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = str(prod[4])
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = str(prod[5])
            precio = SubElement(item, 'dte:Precio')
            precio.text = str(prod[6])
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = str(prod[7])
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
            nombre_corto.text = "IVA"
            codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
            codigo_tax.text = "1"
            taxable = SubElement(impuesto, 'dte:MontoGravable')
            taxable.text = str(prod[8])
            tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
            tax_amount.text = str(prod[10])
            total_line = SubElement(item, 'dte:Total')
            total_line.text = str(prod[11])

        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', str(_iva))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = str(_total)

        # Adenda
        if AdendaSummaryData:
            Adenda = SubElement(sat, 'dte:Adenda')
            AdendaDetail = SubElement(Adenda, 'dte:AdendaDetail')
            AdendaDetail.set('ID', 'AdendaSummary')
            AdendaSummary = SubElement(AdendaDetail, 'dte:AdendaSummary')
            count = 1
            for adsum in AdendaSummaryData:
                val = SubElement(AdendaSummary, 'dte:Valor' + str(count))
                val.text = adsum
                count += 1

        Complementos = SubElement(DatosEmision, 'dte:Complementos')
        Complemento = SubElement(Complementos, 'dte:Complemento')
        Complemento.set('IDComplemento', 'Text')
        Complemento.set('NombreComplemento', 'Text')
        Complemento.set('URIComplemento', 'Text')

        AbonosFacturaCambiaria = SubElement(Complemento, 'cfc:AbonosFacturaCambiaria')
        AbonosFacturaCambiaria.set('xmlns:cfc', 'http://www.sat.gob.gt/dte/fel/CompCambiaria/0.1.0')
        AbonosFacturaCambiaria.set('Version', '1')

        for line in self.megaprint_payment_lines:
            Abono = SubElement(AbonosFacturaCambiaria, 'cfc:Abono')
            NumeroAbono = SubElement(Abono, 'cfc:NumeroAbono')
            NumeroAbono.text = str(line.serial_no or 0)
            FechaVencimiento = SubElement(Abono, 'cfc:FechaVencimiento')
            FechaVencimiento.text = str(line.due_date or 0)
            MontoAbono = SubElement(Abono, 'cfc:MontoAbono')
            MontoAbono.text = str(line.amount or 0)

        rough_string = ET.tostring(fe)
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        #self.xml_request = pretty_str
        return pretty_str

    def GenerateXML_FACT(self, _moneda, _fechayhora, _numeroacceso, _tipo, _afiIVA, _estabCode, _mailEmi, _NITEmisor, _NombreComercial, _NombreEmisor,
                         _calleEmisor, _postalEmisor, _muniEmisor, _deptoEmisor, _paisEmisor, _mailRec, _IDReceptor, _NombreReceptor, _calleRecept,
                         _postalRecept, _muniRecept, _deptoRecept, _paisRecept, _frases, _items, _iva, _total, _uuId, AdendaSummaryData):

        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        fe.set('Version', '0.1')

        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')
        DTE.set('ID', 'DatosCertificados')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', _moneda)
        DatosGenerales.set('FechaHoraEmision', _fechayhora)
        DatosGenerales.set('NumeroAcceso', _numeroacceso)
        DatosGenerales.set('Tipo', _tipo)

        # EMISOR
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        Emisor.set('AfiliacionIVA', _afiIVA)
        Emisor.set('CodigoEstablecimiento', _estabCode)
        Emisor.set('CorreoEmisor', _mailEmi)
        Emisor.set('NITEmisor', _NITEmisor)
        Emisor.set('NombreComercial', _NombreComercial)
        Emisor.set('NombreEmisor', _NombreEmisor)

        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = str(_calleEmisor)

        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = str(_postalEmisor)

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = str(_muniEmisor)

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = str(_deptoEmisor)

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = str(_paisEmisor)

        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', _mailRec)
        Receptor.set('IDReceptor', _IDReceptor)
        Receptor.set('NombreReceptor', _NombreReceptor)

        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = str(_calleRecept)

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = str(_postalRecept)

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = str(_muniRecept)

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = str(_deptoRecept)

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = str(_paisRecept)

        # FRASES
        frases = SubElement(DatosEmision, 'dte:Frases')
        for phrase in _frases:
            frase = SubElement(frases, 'dte:Frase')
            frase.set('CodigoEscenario', str(phrase[0]))
            frase.set('TipoFrase', str(phrase[1]))

        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        for prod in _items:
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', str(prod[0]))
            item.set('NumeroLinea', str(prod[1]))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = str(prod[2])
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = str(prod[3])
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = str(prod[4])
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = str(prod[5])
            precio = SubElement(item, 'dte:Precio')
            precio.text = str(prod[6])
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = str(prod[7])
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
            nombre_corto.text = "IVA"
            codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
            codigo_tax.text = "1"
            taxable = SubElement(impuesto, 'dte:MontoGravable')
            taxable.text = str(prod[8])
            tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
            tax_amount.text = str(prod[10])
            total_line = SubElement(item, 'dte:Total')
            total_line.text = str(prod[11])

        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', str(_iva))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = str(_total)

        # Adenda
        if AdendaSummaryData:
            Adenda = SubElement(sat, 'dte:Adenda')
            AdendaDetail = SubElement(Adenda, 'dte:AdendaDetail')
            AdendaDetail.set('ID', 'AdendaSummary')
            AdendaSummary = SubElement(AdendaDetail, 'dte:AdendaSummary')
            count = 1
            for adsum in AdendaSummaryData:
                val = SubElement(AdendaSummary, 'dte:Valor' + str(count))
                val.text = adsum
                count += 1

        rough_string = ET.tostring(fe, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        return pretty_str

    def GenerateXML_NCRE(self, _moneda, _fechayhora, _numeroacceso, _tipo, _afiIVA, _estabCode, _mailEmi, _NITEmisor, _NombreComercial, _NombreEmisor,
                         _calleEmisor, _postalEmisor, _muniEmisor, _deptoEmisor, _paisEmisor, _mailRec, _IDReceptor, _NombreReceptor, _calleRecept,
                         _postalRecept, _muniRecept, _deptoRecept, _paisRecept, _frases, _items, _iva, _total, _uuId, Complemento_Data, AdendaSummaryData):

        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        #fe.set('xmlns:n1', 'http://www.altova.com/samplexml/other-namespace')
        #fe.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        fe.set('Version', '0.1')

        #fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        #fe.set('xmlns:cfc', 'http://www.sat.gob.gt/dte/fel/CompCambiaria/0.1.0')
        #fe.set('xmlns:cex', 'http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        #fe.set('xmlns:cfe', 'http://www.sat.gob.gt/face2/ComplementoFacturaEspecial/0.1.0')
        #fe.set('xmlns:cno', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')

        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')
        DTE.set('ID', 'DatosCertificados')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', _moneda)
        DatosGenerales.set('FechaHoraEmision', _fechayhora)
        DatosGenerales.set('NumeroAcceso', _numeroacceso)
        DatosGenerales.set('Tipo', _tipo)

        # Emisor
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        Emisor.set('AfiliacionIVA', _afiIVA)
        Emisor.set('CodigoEstablecimiento', _estabCode)
        # Emisor.set('AfiliacionIVA',_estabCode)
        Emisor.set('CorreoEmisor', _mailEmi)
        Emisor.set('NITEmisor', _NITEmisor)
        Emisor.set('NombreComercial', _NombreComercial)
        Emisor.set('NombreEmisor', _NombreEmisor)

        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = str(_calleEmisor)

        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = str(_postalEmisor)

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = str(_muniEmisor)

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = str(_deptoEmisor)

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = str(_paisEmisor)

        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', _mailRec)
        Receptor.set('IDReceptor', _IDReceptor)
        Receptor.set('NombreReceptor', _NombreReceptor)

        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = str(_calleRecept)

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = str(_postalRecept)

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = str(_muniRecept)

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = str(_deptoRecept)

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = str(_paisRecept)

        # FRASES
        #frases = SubElement(DatosEmision, 'dte:Frases')
        #for phrase in _frases:
        #    frase = SubElement(frases, 'dte:Frase')
        #    frase.set('CodigoEscenario', str(phrase[0]))
        #    frase.set('TipoFrase', str(phrase[1]))

        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        for prod in _items:
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', str(prod[0]))
            item.set('NumeroLinea', str(prod[1]))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = str(prod[2])
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = str(prod[3])
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = str(prod[4])
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = str(prod[5])
            precio = SubElement(item, 'dte:Precio')
            precio.text = str(prod[6])
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = str(prod[7])
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
            nombre_corto.text = "IVA"
            codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
            codigo_tax.text = "1"
            taxable = SubElement(impuesto, 'dte:MontoGravable')
            taxable.text = str(prod[8])
            tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
            tax_amount.text = str(prod[10])
            total_line = SubElement(item, 'dte:Total')
            total_line.text = str(prod[11])

        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', str(_iva))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = str(_total)

        # Adenda
        if AdendaSummaryData:
            Adenda = SubElement(sat, 'dte:Adenda')
            AdendaDetail = SubElement(Adenda, 'dte:AdendaDetail')
            AdendaDetail.set('ID', 'AdendaSummary')
            AdendaSummary = SubElement(AdendaDetail, 'dte:AdendaSummary')
            count = 1
            for adsum in AdendaSummaryData:
                val = SubElement(AdendaSummary, 'dte:Valor' + str(count))
                val.text = adsum
                count += 1

        Complementos = SubElement(DatosEmision, 'dte:Complementos')
        Complemento = SubElement(Complementos, 'dte:Complemento')
        Complemento.set('IDComplemento', '1')
        Complemento.set('NombreComplemento', 'NOTA CREDITO')
        Complemento.set('URIComplemento', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')

        ReferenciasNota = SubElement(Complemento, 'cno:ReferenciasNota')
        ReferenciasNota.set('xmlns:cno', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')
        ReferenciasNota.set('FechaEmisionDocumentoOrigen', Complemento_Data['origin_date'])
        # ReferenciasNota.set('MotivoAjuste', 'devolucion')
        ReferenciasNota.set('MotivoAjuste', 'Nota de credito')
        ReferenciasNota.set('NumeroAutorizacionDocumentoOrigen', Complemento_Data['auth_number_doc_origin'])
        ReferenciasNota.set('Version', '0.1')

        rough_string = ET.tostring(fe, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        #self.xml_request = pretty_str
        return pretty_str

    def GenerateXML_EXPORT(self, _moneda,_ex, _fechayhora, _numeroacceso, _tipo, _afiIVA, _estabCode, _mailEmi, _NITEmisor, _NombreComercial, _NombreEmisor,
                         _calleEmisor, _postalEmisor, _muniEmisor, _deptoEmisor, _paisEmisor, _mailRec, _IDReceptor, _NombreReceptor, _calleRecept,
                         _postalRecept, _muniRecept, _deptoRecept, _paisRecept, _frases, _items, _iva, _total, _uuId, AdendaSummaryData, arioODestinatario, DireccionConsign, _OtraReferencia, _INCOTERM, _NombreExportador, _CodigoExportador):
        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        fe.set('Version', '0.1')

        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')
        DTE.set('ID', 'DatosCertificados')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', _moneda)
        if _ex == 'SI' :
            DatosGenerales.set('Exp', _ex)
        DatosGenerales.set('FechaHoraEmision', _fechayhora)
        DatosGenerales.set('NumeroAcceso', _numeroacceso)
        DatosGenerales.set('Tipo', _tipo)

        # EMISOR
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        Emisor.set('AfiliacionIVA', _afiIVA)
        Emisor.set('CodigoEstablecimiento', _estabCode)
        Emisor.set('CorreoEmisor', _mailEmi)
        Emisor.set('NITEmisor', _NITEmisor)
        Emisor.set('NombreComercial', _NombreComercial)
        Emisor.set('NombreEmisor', _NombreEmisor)

        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = str(_calleEmisor)

        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = str(_postalEmisor)

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = str(_muniEmisor)

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = str(_deptoEmisor)

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = str(_paisEmisor)

        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', _mailRec)
        Receptor.set('IDReceptor', _IDReceptor)
        Receptor.set('NombreReceptor', _NombreReceptor)

        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = str(_calleRecept)

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = str(_postalRecept)

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = str(_muniRecept)

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = str(_deptoRecept)

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = str(_paisRecept)

        # FRASES
        frases = SubElement(DatosEmision, 'dte:Frases')
        for phrase in _frases:
            frase = SubElement(frases, 'dte:Frase')
            frase.set('CodigoEscenario', str(phrase[0]))
            frase.set('TipoFrase', str(phrase[1]))

        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        for prod in _items:
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', str(prod[0]))
            item.set('NumeroLinea', str(prod[1]))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = str(prod[2])
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = str(prod[3])
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = str(prod[4])
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = str(prod[5])
            precio = SubElement(item, 'dte:Precio')
            precio.text = str(prod[6])
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = str(prod[7])
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
            nombre_corto.text = "IVA"
            codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
            codigo_tax.text = "2"
            taxable = SubElement(impuesto, 'dte:MontoGravable')
            taxable.text = str(prod[8])
            tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
            tax_amount.text = str(prod[10])
            total_line = SubElement(item, 'dte:Total')
            total_line.text = str(prod[11])

        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', str(_iva))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = str(_total)
        
        # Accessories
        
        Complementos = SubElement(DatosEmision, 'dte:Complementos')
        Complemento = SubElement(Complementos, 'dte:Complemento')
        Complemento.set('IDComplemento', 'Exportacion')
        Complemento.set('NombreComplemento', 'Exportacion')
        Complemento.set('URIComplemento', 'http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        Exportacion = SubElement(Complemento, 'cex:Exportacion')
        Exportacion.set('xmlns:cex','http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        Exportacion.set('Version','1')
        NombreConsignatarioODestinatario = SubElement(Exportacion, 'cex:NombreConsignatarioODestinatario')
        NombreConsignatarioODestinatario.text = arioODestinatario
        DireccionConsignatarioODestinatario = SubElement(Exportacion, 'cex:DireccionConsignatarioODestinatario')
        DireccionConsignatarioODestinatario.text = DireccionConsign
        NombreComprador = SubElement(Exportacion, 'cex:NombreComprador')
        NombreComprador.text = arioODestinatario
        DireccionComprador = SubElement(Exportacion, 'cex:DireccionComprador')
        DireccionComprador.text = DireccionConsign
        OtraReferencia = SubElement(Exportacion, 'cex:OtraReferencia')
        OtraReferencia.text = _OtraReferencia
        INCOTERM = SubElement(Exportacion, 'cex:INCOTERM')
        INCOTERM.text = _INCOTERM
        NombreExportador = SubElement(Exportacion, 'cex:NombreExportador')
        NombreExportador.text = _NombreExportador
        CodigoExportador = SubElement(Exportacion, 'cex:CodigoExportador')
        CodigoExportador.text = _CodigoExportador
        

        # Adenda
        if AdendaSummaryData:
            Adenda = SubElement(sat, 'dte:Adenda')
            AdendaDetail = SubElement(Adenda, 'dte:AdendaDetail')
            AdendaDetail.set('ID', 'AdendaSummary')
            AdendaSummary = SubElement(AdendaDetail, 'dte:AdendaSummary')
            count = 1
            for adsum in AdendaSummaryData:
                val = SubElement(AdendaSummary, 'dte:Valor' + str(count))
                val.text = adsum
                count += 1

        rough_string = ET.tostring(fe, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        return pretty_str

    def GenerateXML_NCRE_EXPORT(self, _moneda, _ex, _fechayhora, _numeroacceso, _tipo, _afiIVA, _estabCode, _mailEmi, _NITEmisor, _NombreComercial, _NombreEmisor,
                         _calleEmisor, _postalEmisor, _muniEmisor, _deptoEmisor, _paisEmisor, _mailRec, _IDReceptor, _NombreReceptor, _calleRecept,
                         _postalRecept, _muniRecept, _deptoRecept, _paisRecept, _frases, _items, _iva, _total, _uuId, Complemento_Data, AdendaSummaryData, arioODestinatario, DireccionConsign, _OtraReferencia, _INCOTERM, _NombreExportador, _CodigoExportador):

        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        #fe.set('xmlns:n1', 'http://www.altova.com/samplexml/other-namespace')
        #fe.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        fe.set('Version', '0.1')

        #fe.set('xmlns:xd', 'http://www.w3.org/2000/09/xmldsig#')
        #fe.set('xmlns:cfc', 'http://www.sat.gob.gt/dte/fel/CompCambiaria/0.1.0')
        #fe.set('xmlns:cex', 'http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        #fe.set('xmlns:cfe', 'http://www.sat.gob.gt/face2/ComplementoFacturaEspecial/0.1.0')
        #fe.set('xmlns:cno', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')

        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')
        DTE.set('ID', 'DatosCertificados')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', _moneda)
        if _ex == 'SI' :
            DatosGenerales.set('Exp', _ex)
        DatosGenerales.set('FechaHoraEmision', _fechayhora)
        DatosGenerales.set('NumeroAcceso', _numeroacceso)
        DatosGenerales.set('Tipo', _tipo)

        # Emisor
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        Emisor.set('AfiliacionIVA', _afiIVA)
        Emisor.set('CodigoEstablecimiento', _estabCode)
        # Emisor.set('AfiliacionIVA',_estabCode)
        Emisor.set('CorreoEmisor', _mailEmi)
        Emisor.set('NITEmisor', _NITEmisor)
        Emisor.set('NombreComercial', _NombreComercial)
        Emisor.set('NombreEmisor', _NombreEmisor)

        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = str(_calleEmisor)

        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = str(_postalEmisor)

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = str(_muniEmisor)

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = str(_deptoEmisor)

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = str(_paisEmisor)

        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', _mailRec)
        Receptor.set('IDReceptor', _IDReceptor)
        Receptor.set('NombreReceptor', _NombreReceptor)

        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = str(_calleRecept)

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = str(_postalRecept)

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = str(_muniRecept)

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = str(_deptoRecept)

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = str(_paisRecept)

        # FRASES
        frases = SubElement(DatosEmision, 'dte:Frases')
        for phrase in _frases:
            frase = SubElement(frases, 'dte:Frase')
            frase.set('CodigoEscenario', str(phrase[0]))
            frase.set('TipoFrase', str(phrase[1]))

        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        for prod in _items:
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', str(prod[0]))
            item.set('NumeroLinea', str(prod[1]))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = str(prod[2])
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = str(prod[3])
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = str(prod[4])
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = str(prod[5])
            precio = SubElement(item, 'dte:Precio')
            precio.text = str(prod[6])
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = str(prod[7])
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
            nombre_corto.text = "IVA"
            codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
            codigo_tax.text = "2"
            taxable = SubElement(impuesto, 'dte:MontoGravable')
            taxable.text = str(prod[8])
            tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
            tax_amount.text = str(prod[10])
            total_line = SubElement(item, 'dte:Total')
            total_line.text = str(prod[11])

        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', str(_iva))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = str(_total)

        # Adenda
        if AdendaSummaryData:
            Adenda = SubElement(sat, 'dte:Adenda')
            AdendaDetail = SubElement(Adenda, 'dte:AdendaDetail')
            AdendaDetail.set('ID', 'AdendaSummary')
            AdendaSummary = SubElement(AdendaDetail, 'dte:AdendaSummary')
            count = 1
            for adsum in AdendaSummaryData:
                val = SubElement(AdendaSummary, 'dte:Valor' + str(count))
                val.text = adsum
                count += 1

        Complementos = SubElement(DatosEmision, 'dte:Complementos')
        Complemento = SubElement(Complementos, 'dte:Complemento')
        Complemento.set('IDComplemento', '1')
        Complemento.set('NombreComplemento', 'NOTA CREDITO')
        Complemento.set('URIComplemento', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')

        ReferenciasNota = SubElement(Complemento, 'cno:ReferenciasNota')
        ReferenciasNota.set('xmlns:cno', 'http://www.sat.gob.gt/face2/ComplementoReferenciaNota/0.1.0')
        ReferenciasNota.set('FechaEmisionDocumentoOrigen', Complemento_Data['origin_date'])
        # ReferenciasNota.set('MotivoAjuste', 'devolucion')
        ReferenciasNota.set('MotivoAjuste', 'Nota de credito')
        ReferenciasNota.set('NumeroAutorizacionDocumentoOrigen', Complemento_Data['auth_number_doc_origin'])
        ReferenciasNota.set('Version', '0.1')
        #Complemento de exportacion
        Complemento2 = SubElement(Complementos, 'dte:Complemento')
        Complemento2.set('IDComplemento', 'Exportacion')
        Complemento2.set('NombreComplemento', 'Exportacion')
        Complemento2.set('URIComplemento', 'http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        Exportacion = SubElement(Complemento2, 'cex:Exportacion')
        Exportacion.set('xmlns:cex','http://www.sat.gob.gt/face2/ComplementoExportaciones/0.1.0')
        Exportacion.set('Version','1')
        NombreConsignatarioODestinatario = SubElement(Exportacion, 'cex:NombreConsignatarioODestinatario')
        NombreConsignatarioODestinatario.text = arioODestinatario
        DireccionConsignatarioODestinatario = SubElement(Exportacion, 'cex:DireccionConsignatarioODestinatario')
        DireccionConsignatarioODestinatario.text = DireccionConsign
        NombreComprador = SubElement(Exportacion, 'cex:NombreComprador')
        NombreComprador.text = arioODestinatario
        DireccionComprador = SubElement(Exportacion, 'cex:DireccionComprador')
        DireccionComprador.text = DireccionConsign
        OtraReferencia = SubElement(Exportacion, 'cex:OtraReferencia')
        OtraReferencia.text = _OtraReferencia
        INCOTERM = SubElement(Exportacion, 'cex:INCOTERM')
        INCOTERM.text = _INCOTERM
        NombreExportador = SubElement(Exportacion, 'cex:NombreExportador')
        NombreExportador.text = _NombreExportador
        CodigoExportador = SubElement(Exportacion, 'cex:CodigoExportador')
        CodigoExportador.text = _CodigoExportador

        rough_string = ET.tostring(fe, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        #self.xml_request = pretty_str
        return pretty_str

    def GenerateXML_FESP(self, data={}):

        fe = Element('dte:GTDocumento')
        fe.set('xmlns:dte', 'http://www.sat.gob.gt/dte/fel/0.2.0')
        fe.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        fe.set('Version', '0.1')
        
        sat = SubElement(fe, 'dte:SAT')
        sat.set('ClaseDocumento', 'dte')

        DTE = SubElement(sat, 'dte:DTE')
        DTE.set('ID', 'DatosCertificados')

        DatosEmision = SubElement(DTE, 'dte:DatosEmision')
        DatosEmision.set('ID', 'DatosEmision')

        DatosGenerales = SubElement(DatosEmision, 'dte:DatosGenerales')
        DatosGenerales.set('CodigoMoneda', data.get('moneda', ''))
        DatosGenerales.set('FechaHoraEmision', data.get('date_dte', ''))
        DatosGenerales.set('Tipo', data.get('tipo', ''))
        
        # Emisor
        Emisor = SubElement(DatosEmision, 'dte:Emisor')
        if data.get('regimeniva', ''):
            Emisor.set('AfiliacionIVA', data.get('regimeniva', '')) 
        Emisor.set('CodigoEstablecimiento', data.get('establecimiento', ''))
        Emisor.set('NITEmisor', data.get('nitemisor', ''))
        Emisor.set('NombreComercial', data.get('nombrecomercial', ''))
        Emisor.set('NombreEmisor', data.get('nombreemisor', ''))
        
        DireccionEmisor = SubElement(Emisor, 'dte:DireccionEmisor')

        calleEmisor = SubElement(DireccionEmisor, 'dte:Direccion')
        calleEmisor.text = data.get('calleemisor', '')
        
        postalEmisor = SubElement(DireccionEmisor, 'dte:CodigoPostal')
        postalEmisor.text = data.get('postalemisor', '')

        municipioEmisor = SubElement(DireccionEmisor, 'dte:Municipio')
        municipioEmisor.text = data.get('municipioemisor', '')

        departamentoEmisor = SubElement(DireccionEmisor, 'dte:Departamento')
        departamentoEmisor.text = data.get('departamentoemisor', '')

        paisEmisor = SubElement(DireccionEmisor, 'dte:Pais')
        paisEmisor.text = data.get('paisemisor', '')
        
        # RECEPTOR
        Receptor = SubElement(DatosEmision, 'dte:Receptor')
        Receptor.set('CorreoReceptor', data.get('correoreceptor', ''))
        Receptor.set('IDReceptor', data.get('nitreceptor', ''))
        Receptor.set('NombreReceptor', data.get('nombrereceptor', ''))
        if data.get('TipoDocu', '') != 'NIT':
            Receptor.set('TipoEspecial', data.get('TipoDocu', ''))
            
        DireccionReceptor = SubElement(Receptor, 'dte:DireccionReceptor')

        calleRecept = SubElement(DireccionReceptor, 'dte:Direccion')
        calleRecept.text = data.get('callereceptor', '')

        postalRecept = SubElement(DireccionReceptor, 'dte:CodigoPostal')
        postalRecept.text = data.get('postalreceptor', '')

        municipioRecept = SubElement(DireccionReceptor, 'dte:Municipio')
        municipioRecept.text = data.get('municipiorecptor', '')

        departamentoRecept = SubElement(DireccionReceptor, 'dte:Departamento')
        departamentoRecept.text = data.get('departamentoreceptor', '')

        paisRecept = SubElement(DireccionReceptor, 'dte:Pais')
        paisRecept.text = data.get('paisreceptor', '')

        # FRASES
        #frases = SubElement(DatosEmision, 'dte:Frases')
        #for phrase in _frases:
        #    frase = SubElement(frases, 'dte:Frase')
        #    frase.set('CodigoEscenario', str(phrase[0]))
        #    frase.set('TipoFrase', str(phrase[1]))
        
        # ITEMS
        items = SubElement(DatosEmision, 'dte:Items')
        #raise UserError(('%s') %(data.get('items', [])))
        for line in data.get('items', []):
            item = SubElement(items, 'dte:Item')
            item.set('BienOServicio', line.get('tipoitem', ''))
            item.set('NumeroLinea', line.get('line', ''))
            cantidad = SubElement(item, 'dte:Cantidad')
            cantidad.text = line.get('cantidad', '')
            uom = SubElement(item, 'dte:UnidadMedida')
            uom.text = line.get('uom', '')
            descripcion = SubElement(item, 'dte:Descripcion')
            descripcion.text = line.get('descripcion', '')
            precio_unitario = SubElement(item, 'dte:PrecioUnitario')
            precio_unitario.text = line.get('preciounitario', '')
            precio = SubElement(item, 'dte:Precio')
            precio.text = line.get('subtotal', '')
            descuento = SubElement(item, 'dte:Descuento')
            descuento.text = line.get('descuento', '')
            impuestos = SubElement(item, 'dte:Impuestos')
            impuesto = SubElement(impuestos, 'dte:Impuesto')
            for tax in line.get('itemsimpuestos', []):
                nombre_corto = SubElement(impuesto, 'dte:NombreCorto')
                nombre_corto.text = tax.get('tax_name', '')
                codigo_tax = SubElement(impuesto, 'dte:CodigoUnidadGravable')
                codigo_tax.text = "1"
                taxable = SubElement(impuesto, 'dte:MontoGravable')
                taxable.text = tax.get('base', '')
                tax_amount = SubElement(impuesto, 'dte:MontoImpuesto')
                tax_amount.text = tax.get('tax', '')
            total_line = SubElement(item, 'dte:Total')
            total_line.text = line.get('subtotal', '')
            
        # TOTALES
        totales = SubElement(DatosEmision, 'dte:Totales')
        listaImpuestos = SubElement(totales, 'dte:TotalImpuestos')
        totalImpuesto = SubElement(listaImpuestos, 'dte:TotalImpuesto')
        totalImpuesto.set('NombreCorto', 'IVA')
        totalImpuesto.set('TotalMontoImpuesto', data.get('totalimpuestos', ''))

        granTotal = SubElement(totales, 'dte:GranTotal')
        granTotal.text = data.get('total', '')
        
        # Adenda
        #if data.get('adenda', False):
        #    Adenda = SubElement(sat, 'dte:Adenda')
        #    AdendaDetail = SubElement(Adenda, 'dtecomm:Informacion_COMERCIAL')
        #    AdendaDetail.set('xsi:schemaLocation', 'https://www.digifact.com.gt/dtecomm')
        #    AdendaDetail.set('xmlns:dtecomm', 'https://www.digifact.com.gt/dtecomm')
        #    AdendaSummary = SubElement(AdendaDetail, 'dtecomm:InformacionAdicional')
        #    AdendaSummary.set('Version', '7.1234654163')
        #    for item in data.get('adenda', []):
        #        for key, value in item.items():
        #            val = SubElement(AdendaSummary, 'dtecomm:' + str(key))
        #            val.text = str(value)

        #Complementos FESP
        items_complementos = data.get('complementos', {})
#         items_complementos = data.get('complementos')
        Complementos = SubElement(DatosEmision, 'dte:Complementos')
        Complemento = SubElement(Complementos, 'dte:Complemento')
        Complemento.set('NombreComplemento', 'RETENCION')
        Complemento.set('URIComplemento', 'http://www.sat.gob.gt/face2/ComplementoFacturaEspecial/0.1.0')
        Complemento.set('IDComplemento', '1')
        
        #Datos de retencion de FESP
        ReferenciasFESP = SubElement(Complemento, 'cfe:RetencionesFacturaEspecial')
        ReferenciasFESP.set('xmlns:cfe', 'http://www.sat.gob.gt/face2/ComplementoFacturaEspecial/0.1.0')
        ReferenciasFESP.set('Version', '1')
        for item in items_complementos:
            RetESP = SubElement(ReferenciasFESP, 'cfe:' + str(item.get('EtiquetaFel', '')))
            RetESP.text = item.get('Amount', 0.00)
        
        rough_string = ET.tostring(fe, encoding='utf-8', method='xml')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        return pretty_str