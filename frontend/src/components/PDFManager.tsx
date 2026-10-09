'use client';

import React, { useState, useRef } from 'react';
import {
  Upload,
  FileText,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Clock,
  Sparkles,
  FileCheck,
  ChevronRight
} from 'lucide-react';
import { DocumentMetadata } from '../types';
import { uploadPDF, deleteDocument } from '../lib/api';

interface PDFManagerProps {
  documents: DocumentMetadata[];
  setDocuments: React.Dispatch<React.SetStateAction<DocumentMetadata[]>>;
  activeDocumentId: string | null;
  setActiveDocumentId: (id: string | null) => void;
  onDocumentSelectForChat?: (doc: DocumentMetadata) => void;
}

export const PDFManager: React.FC<PDFManagerProps> = ({
  documents,
  setDocuments,
  activeDocumentId,
  setActiveDocumentId,
  onDocumentSelectForChat
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const file = files[0];

    // Validate PDF
    if (!file.name.toLowerCase().endsWith('.pdf') && file.type !== 'application/pdf') {
      setUploadError('Only PDF documents are supported. Please select a valid .pdf file.');
      return;
    }

    // Validate size (max 25MB)
    if (file.size > 25 * 1024 * 1024) {
      setUploadError('File is too large. Maximum supported PDF size is 25MB.');
      return;
    }

    setUploadError(null);
    setIsUploading(true);

    try {
      const metadata = await uploadPDF(file);
      setDocuments((prev) => [metadata, ...prev]);
      // Automatically select uploaded document
      setActiveDocumentId(metadata.id);
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload and parse document');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (docId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to remove this document and its citations?')) return;

    try {
      await deleteDocument(docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
      if (activeDocumentId === docId) {
        setActiveDocumentId(null);
      }
    } catch (err: any) {
      alert('Could not delete document: ' + err.message);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/60 to-slate-900 p-6 border border-indigo-500/20 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <FileCheck className="h-4 w-4" />
              <span>RAG Document Library</span>
            </div>
            <h2 className="text-2xl font-bold text-white mt-1">
              Upload Coursework, Textbooks &amp; Notes
            </h2>
            <p className="text-slate-300 text-sm mt-1 max-w-2xl">
              Upload your syllabus or lecture slides. LearnBridge AI extracts page-by-page text,
              indexes it for precision Retrieval-Augmented Generation (RAG), and provides exact page citations.
              <span className="text-emerald-400 font-medium"> PDF upload is completely optional!</span>
            </p>
          </div>

          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="flex items-center justify-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-sm shadow-lg shadow-indigo-500/25 transition-all transform hover:-translate-y-0.5 active:translate-y-0 shrink-0"
          >
            <Upload className="h-4 w-4" />
            <span>{isUploading ? 'Extracting Text...' : 'Upload PDF Document'}</span>
          </button>
        </div>
      </div>

      {/* Drag & Drop Upload Zone */}
      <div
        onDragEnter={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setDragActive(false);
        }}
        onDrop={(e) => {
          e.preventDefault();
          setDragActive(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
          dragActive
            ? 'border-indigo-400 bg-indigo-500/10 scale-[1.01]'
            : 'border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/60'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />

        <div className="h-14 w-14 mx-auto rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-3 shadow-inner">
          <Upload className={`h-7 w-7 ${isUploading ? 'animate-bounce' : ''}`} />
        </div>

        <h3 className="text-base font-semibold text-white">
          {isUploading ? 'Parsing Pages with PyMuPDF...' : 'Drag & Drop PDF here, or browse files'}
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Supports searchable &amp; scanned textbooks, lecture notes, question banks up to 25MB
        </p>

        {uploadError && (
          <div className="mt-4 inline-flex items-center space-x-2 px-4 py-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{uploadError}</span>
          </div>
        )}
      </div>

      {/* Uploaded Documents List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <h3 className="text-lg font-bold text-white">Your Uploaded Documents</h3>
            <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 text-xs font-semibold">
              {documents.length}
            </span>
          </div>
          {activeDocumentId && (
            <button
              onClick={() => setActiveDocumentId(null)}
              className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
            >
              Clear Active Selection (Switch to General AI)
            </button>
          )}
        </div>

        {documents.length === 0 ? (
          <div className="rounded-xl border border-slate-800/80 bg-slate-900/30 p-8 text-center">
            <FileText className="h-10 w-10 text-slate-600 mx-auto mb-2" />
            <p className="text-slate-400 text-sm font-medium">No documents uploaded yet.</p>
            <p className="text-slate-500 text-xs mt-1">
              You can ask questions directly in General AI mode without uploading a document.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {documents.map((doc) => {
              const isSelected = activeDocumentId === doc.id;
              return (
                <div
                  key={doc.id}
                  onClick={() => {
                    setActiveDocumentId(isSelected ? null : doc.id);
                    if (onDocumentSelectForChat) onDocumentSelectForChat(doc);
                  }}
                  className={`group relative rounded-xl p-5 border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-indigo-950/40 border-indigo-500/80 shadow-lg shadow-indigo-500/15 ring-1 ring-indigo-500'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3">
                      <div
                        className={`h-10 w-10 rounded-lg flex items-center justify-center shrink-0 ${
                          isSelected ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        <FileText className="h-5 w-5" />
                      </div>
                      <div className="min-w-0 pr-2">
                        <h4 className="text-sm font-semibold text-white truncate group-hover:text-indigo-300 transition-colors">
                          {doc.filename}
                        </h4>
                        <div className="flex items-center space-x-2 text-[11px] text-slate-400 mt-1">
                          <span>{doc.total_pages} {doc.total_pages === 1 ? 'page' : 'pages'}</span>
                          <span>•</span>
                          <span>{formatFileSize(doc.file_size_bytes)}</span>
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={(e) => handleDelete(doc.id, e)}
                      title="Delete document"
                      className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>

                  {doc.summary_preview && (
                    <p className="text-xs text-slate-400 line-clamp-2 mt-3 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800/50">
                      {doc.summary_preview}
                    </p>
                  )}

                  <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                    <div className="flex items-center space-x-1.5">
                      <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span className="text-[11px] font-medium text-emerald-400">Indexed for RAG</span>
                    </div>

                    <span
                      className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                        isSelected
                          ? 'bg-indigo-500 text-white'
                          : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'
                      }`}
                    >
                      {isSelected ? 'Active Source' : 'Select'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
