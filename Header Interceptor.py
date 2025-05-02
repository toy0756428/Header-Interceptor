# -*- coding: utf-8 -*-
from burp import IBurpExtender, IHttpListener, ITab
from java.awt import BorderLayout, Dimension, FlowLayout, Color
import javax.swing as swing
from java.lang import Runnable, Thread, Runtime
from java.awt.event import ActionListener
import java.io.BufferedReader as BufferedReader
import java.io.InputStreamReader as InputStreamReader


class BurpExtender(IBurpExtender, IHttpListener, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("Header Interceptor")
        callbacks.registerHttpListener(self)

        # GUI
        self._build_gui()

        # Burp
        callbacks.addSuiteTab(self)

    def getTabCaption(self):
        return "Header Interceptor"

    def getUiComponent(self):
        return self._main_panel

    def _build_gui(self):
        self._main_panel = swing.JPanel(BorderLayout())
        self._main_panel.setBackground(Color(245, 245, 245))

        # System Message
        self.message_area = swing.JTextArea(10, 80)
        self.message_area.setEditable(False)
        self.message_area.setLineWrap(True)
        self.message_area.setWrapStyleWord(True)
        self.message_area.setBackground(Color(235, 235, 235))
        message_scroll = swing.JScrollPane(self.message_area)

        # Header
        self.header_area = swing.JTextArea(10, 80)
        self.header_area.setEditable(False)
        self.header_area.setLineWrap(True)
        self.header_area.setWrapStyleWord(True)
        self.message_area.setBackground(Color(235, 235, 235))
        header_scroll = swing.JScrollPane(self.header_area)

        # Filter
        filter_panel = swing.JPanel()
        filter_panel.add(swing.JLabel("Filter Header:"))
        self.header_filter_field = swing.JTextField(20)
        filter_panel.add(self.header_filter_field)

        # Button
        button_panel = swing.JPanel()
        start_button = swing.JButton("Start")
        clear_button = swing.JButton("Clear")
        start_button.addActionListener(StartButtonListener(self))
        clear_button.addActionListener(ClearButtonListener(self))
        button_panel.add(start_button)
        button_panel.add(clear_button)

        center_panel = swing.JPanel(BorderLayout())
        center_panel.add(filter_panel, BorderLayout.NORTH)
        center_panel.add(header_scroll, BorderLayout.CENTER)
        center_panel.add(button_panel, BorderLayout.SOUTH)

        self._main_panel.add(message_scroll, BorderLayout.NORTH)
        self._main_panel.add(center_panel, BorderLayout.CENTER)

    def run_selenium(self):
        try:
            process = Runtime.getRuntime().exec(
                "/path/to/python3 /path/to/selenium_script.py"
            )
            std_input = BufferedReader(InputStreamReader(process.getInputStream()))
            std_error = BufferedReader(InputStreamReader(process.getErrorStream()))

            line = std_input.readLine()
            while line:
                self.message_area.append("[OUT] {}\n".format(line))
                line = std_input.readLine()

            line = std_error.readLine()
            while line:
                self.message_area.append("[ERR] {}\n".format(line))
                line = std_error.readLine()

            process.waitFor()
            self.message_area.append("[*] Selenium finished.\n")
        except Exception as e:
            self.message_area.append("[!] Selenium error: {}\n".format(str(e)))

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if messageIsRequest:
            request_info = self._helpers.analyzeRequest(messageInfo)
            headers = request_info.getHeaders()
            keyword = self.header_filter_field.getText().strip()

            for header in headers:
                if keyword and keyword.lower() in header.lower():
                    self.header_area.append("[Header Match] {}\n".format(header))


class StartButtonListener(ActionListener):
    def __init__(self, extender):
        self.extender = extender

    def actionPerformed(self, event):
        self.extender.message_area.append("[*] Starting Selenium...\n")
        t = Thread(RunnableAdapter(self.extender.run_selenium))
        t.start()


class ClearButtonListener(ActionListener):
    def __init__(self, extender):
        self.extender = extender

    def actionPerformed(self, event):
        self.extender.message_area.setText("")
        self.extender.header_area.setText("")


class RunnableAdapter(Runnable):
    def __init__(self, func):
        self.func = func

    def run(self):
        self.func()
